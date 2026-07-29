---
name: Model Context Protocol
aliases: [MCP, Model Context Protocol, protocollo MCP]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-07-29
---

# Model Context Protocol

## Cos'e

Model Context Protocol (MCP) e' un protocollo aperto, basato su JSON-RPC 2.0, che standardizza il modo in cui le applicazioni AI espongono e consumano contesto: tool, dati, prompt template, accesso a sistemi esterni. E' stato pubblicato da Anthropic nel novembre 2024 come specifica open source con SDK in TypeScript, Python, Go, Java, Rust, C# e altri linguaggi. L'analogia ricorrente e' "USB-C per gli LLM": un'interfaccia uniforme tra modello e mondo, che sostituisce le integrazioni N x M (N modelli x M tool) con N + M.

Il problema che MCP risolve nasce dalla diffusione del [tool use](./tool-use.md) negli [agent](./agent.md). Prima di MCP, ogni framework aveva il proprio formato di descrizione tool, ogni applicazione integrava sistemi esterni con codice ad-hoc, ogni connettore Slack o GitHub veniva riscritto in dozzine di repository. MCP definisce un'API neutrale: un MCP server espone capacita' (tools, resources, prompts), un MCP client (un'app come Claude Desktop, Cursor, un agent SDK) le consuma. La stessa configurazione di server funziona con qualunque modello e qualunque client conforme.

L'adozione e' stata rapida e nella primavera 2026 e' di fatto completata sul piano dei grandi lab. Tra il 2024 e il 2026 OpenAI ha aggiunto supporto MCP in ChatGPT desktop e Agents SDK; Google nel Gemini SDK e, nel maggio 2026, ha iniziato a pubblicare MCP server gestiti per le proprie API cloud (vedi sotto); IDE come Cursor, Windsurf, JetBrains, VS Code lo supportano nativamente. Nel novembre 2025, in occasione del primo anniversario, e' uscita la revisione di specifica 2025-11-25 con feature mature (Tasks asincroni, elicitation, extensions), ed e' stato consolidato un registry ufficiale (registry.modelcontextprotocol.io) che a fine maggio 2026 conta diverse migliaia di server pubblicati. MCP e' diventato lo strato di interoperabilita' di fatto per agenti, in modo analogo a come HTTP lo e' per il web e LSP per gli editor di codice.

## Come funziona

MCP definisce due ruoli e tre primitive principali. I ruoli sono client (l'app AI o l'agente) e server (espone capacita'). Le primitive sono:

Tools. Funzioni invocabili dal modello. Hanno nome, descrizione, input schema (JSON Schema), e ritornano contenuto (testo, immagine, embedded resource). Esempio: `create_issue(repo, title, body)` esposto da un GitHub MCP server. Il modello vede la descrizione e decide quando chiamare il tool; il client esegue la chiamata RPC al server e restituisce il risultato al modello.

Resources. Dati indirizzabili con URI (`file://`, `postgres://`, `slack://channel/123`). Sono passivi: il server li espone, il client li include nel contesto su richiesta dell'utente o dell'app. Servono per dare al modello accesso a documenti, query di database, log, senza che il modello debba "chiamarli". La distinzione tools vs resources e' application-controlled vs user-controlled: i tool sono decisi dal modello, le resource selezionate dall'utente o dall'app.

Prompts. Template di prompt parametrizzati che l'utente puo' invocare come slash command. Servono per workflow ripetibili (es. `/code-review pr_url`) standardizzati tra applicazioni.

Trasporto. MCP supporta tre trasporti. Stdio: il server gira come processo locale, comunicazione su stdin/stdout. Adatto a tool che girano sulla macchina dell'utente (filesystem, git, bash). Streamable HTTP: il server e' un endpoint HTTP che supporta long-running streams via Server-Sent Events. Adatto a server remoti, multi-tenant, deployabili come microservizi. (Una versione precedente "HTTP+SSE" e' stata rimpiazzata da Streamable HTTP nella spec 2025-03-26.) WebSocket: meno usato, supportato in alcuni SDK.

Lifecycle. Il client all'avvio invia `initialize` dichiarando capacita' supportate (sampling, roots, elicitation) e versione protocollo; il server risponde con le proprie capacita' e l'elenco di tools, resources, prompts. Da quel momento il client puo' inviare `tools/list`, `tools/call`, `resources/read`, `prompts/get`. Il server puo' anche inviare richieste sampling al client (chiedere al modello di fare una chiamata LLM, lasciando il modello e i token al client).

Tasks (operazioni asincrone). La revisione 2025-11-25 introduce un primitivo sperimentale Tasks che trasforma qualunque richiesta in un'operazione "call-now, fetch-later": una richiesta puo' restituire un task handle, il client interroga lo stato e recupera il risultato in seguito. Un task attraversa stati come `working`, `input_required`, `completed`, `failed`, `cancelled`. Questo risolve un limite pratico evidente quando un MCP server orchestra operazioni lunghe (build, query pesanti, workflow multi-step) che eccedono i timeout di una singola chiamata sincrona, ed e' la base per agenti che lanciano lavoro in background.

Elicitation. La spec 2025-11-25 formalizza la URL Mode Elicitation (SEP-1036): invece di chiedere credenziali dentro il client MCP, il server puo' restituire un URL e far completare all'utente il flusso sensibile nel browser (OAuth, pagamenti, immissione di API key). Sposta i secret fuori dal canale dell'agente, riducendo la superficie di leakage.

Sampling con tool. SEP-1577 (Sampling with Tools) colma un gap per i workflow agentici: prima il sampling iniziato dal server non poteva includere tool; ora un MCP server puo' avviare richieste sampling con definizioni di tool, abilitando loop agentici lato server.

Sicurezza. La spec impone consenso esplicito dell'utente per tool execution, per resource exposure, per sampling. Le applicazioni client devono mostrare quale server sta eseguendo cosa. La superficie d'attacco principale (prompt injection da contenuto restituito dai tool, server malevoli che esfiltrano dati) e' coperta da raccomandazioni operative: sandbox dei server, audit log, allowlist. Sul fronte authorization, la spec 2025-11-25 aggiunge Authorization Extensions, a partire dal supporto OAuth client-credentials per flussi machine-to-machine (SEP-1046), utile per server interni invocati da agenti senza un utente interattivo.

## Varianti / approcci

MCP non ha "varianti" in senso architetturale ma ha pattern di deployment differenti.

| Pattern | Trasporto | Uso |
|---|---|---|
| Local-first server | stdio | Tool che operano su file locali, repo, container dell'utente |
| Remote SaaS server | streamable HTTP | Integrazioni con servizi cloud (Slack, Notion, Linear, GitHub) |
| Internal enterprise server | HTTP, autenticato | Strumenti aziendali (CRM, ERP, datawarehouse) |
| Vendor-managed server | HTTP, multi-tenant | Server ufficiali pubblicati dal provider dell'API (es. Google Pay & Wallet, Moody's, Westlaw) |
| Marketplace server | HTTP, multi-tenant | Server condivisi pubblicati su registry pubblici |

Un'evoluzione strutturale della primavera 2026 e' proprio l'emergere dei vendor-managed server: il provider di un servizio pubblica e mantiene direttamente un MCP server ufficiale sopra le proprie API, eliminando i wrapper manuali costruiti dagli sviluppatori. Google ha reso disponibili MCP server gestiti per le proprie API cloud e ha lanciato il Google Pay & Wallet Developer MCP Server; Moody's espone un MCP connector con dati su 600+ milioni di aziende; Thomson Reuters un connettore MCP verso Westlaw, Practical Law e KeyCite per CoCounsel.

Confronto con alternative.

| Approccio | Pro | Contro |
|---|---|---|
| MCP | Standard aperto, ecosistema crescente, neutralita' | Overhead di setup, stato in evoluzione |
| Function calling proprietario (OpenAI tools, Anthropic tools) | Semplice, integrato | Vendor lock-in, non interoperabile |
| Plugin proprietari (es. ChatGPT plugins, dismessi) | UX integrata | Ecosistema chiuso, deprecato |
| OpenAPI / REST diretto | Standard maturo | Manca contratto pensato per LLM (descrizioni semantiche) |
| LangChain Tools | Ricco, Python-first | Lock-in al framework |

Una scelta progettuale tipica e' usare MCP per i tool di sistema/dominio e mantenere il function calling nativo per tool ad-hoc tightly coupled all'app. E' interessante notare che la generazione automatica di SDK e MCP server da specifiche OpenAPI e' diventata un layer infrastrutturale conteso: l'azienda Stainless, che generava SDK e MCP server in produzione per OpenAI, Google, Cloudflare e per gli stessi SDK ufficiali Anthropic, e' stata acquisita da Anthropic nel maggio 2026, con chiusura dei prodotti hosted — segnale di quanto la toolchain MCP/SDK sia considerata strategica.

## Quando usarlo / quando no

MCP e' la scelta giusta quando si costruisce un agente che integra molti tool eterogenei, quando si vuole esporre capacita' a piu' modelli/client senza riscrivere codice, quando l'organizzazione vuole un layer di tool centralizzato e auditabile, quando si lavora su un IDE o desktop client che gia' supporta MCP, e quando esiste gia' un server ufficiale del vendor del servizio che si vuole integrare (in quel caso conviene consumarlo invece di costruire un wrapper). Esempi: agenti di coding che usano filesystem + git + bash + linguaggi-specifici; assistenti aziendali che orchestrano Slack, Linear, Notion; strumenti di data analytics che combinano database + filesystem + LLM; integrazioni di pagamento agentiche che consumano un MCP server di Google Pay.

MCP e' la scelta sbagliata quando si fa una singola chiamata LLM con un solo tool deterministico (overkill), quando la latenza extra del trasporto e' inaccettabile (microsecond budget), quando il tool e' un dettaglio interno dell'app e non andra' mai esposto altrove, quando si lavora in un ambiente che non supporta i client MCP.

Anti-pattern. Esporre 100+ tool indiscriminatamente: il modello sceglie peggio. Server senza autenticazione su rete pubblica: rischio sicurezza. Confondere tool e resource (mettere tutto come tool spinge l'agente a "cercare" dati che dovrebbero essere passivi). Reinventare descrizioni: la qualita' del campo `description` e dello schema input determina la qualita' delle chiamate del modello. Installare server da registry pubblici senza verificarne la provenienza: equivale a eseguire un binario arbitrario. Usare operazioni sincrone bloccanti per workflow lunghi quando il primitivo Tasks (2025-11-25) e' progettato esattamente per quel caso.

## Esempi pratici

Esempio 1: server MCP minimale in Python.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_forecast(city: str, days: int = 1) -> str:
    """Restituisce le previsioni meteo per una citta'."""
    # ... chiamata API meteo ...
    return f"Previsioni per {city} ({days} giorni): sereno, 22 C"

if __name__ == "__main__":
    mcp.run()  # stdio transport
```

Configurazione lato Claude Desktop in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

Esempio 2: server remoto enterprise con tunnel. Un MCP server espone tool `query_warehouse(sql)` autenticato con OAuth2 su HTTPS. L'agente di un analista invoca il tool, riceve dati tabellari, li sintetizza. La governance dell'azienda controlla policy SQL (deny su DROP, rate limiting per utente) lato server, indipendentemente dal client AI. Nelle architetture enterprise piu' recenti (es. Claude Managed Agents) il server vive nella rete privata aziendale e l'agente lo raggiunge tramite un MCP tunnel: un gateway outbound-only, senza regole di firewall inbound ne' endpoint pubblici, traffico cifrato end-to-end. Il loop agentico resta sul provider, l'esecuzione del tool e i dati restano nel perimetro del cliente.

Esempio 3: combinazione tools + resources. Un MCP server di un repository git espone come resources i file (`file://path`) e come tools `git_diff`, `git_log`, `git_blame`. L'utente puo' aggiungere file specifici al contesto via resource (li mostra; il modello li legge), il modello puo' chiamare i tool quando serve aggregazione storica. Questo separa input deliberato (l'utente sceglie cosa mettere in contesto) da azione autonoma (l'agente decide cosa interrogare).

Esempio 4: operazione asincrona con Tasks. Un MCP server di build espone `run_build(target)`. Con il primitivo Tasks della spec 2025-11-25, la chiamata ritorna immediatamente un task handle in stato `working`; il client interroga lo stato (`input_required` se serve conferma, poi `completed` o `failed`) e recupera il risultato al termine, senza tenere bloccata la chiamata RPC per minuti.

## Letture

- Anthropic, "Introducing the Model Context Protocol", novembre 2024. https://www.anthropic.com/news/model-context-protocol
- Specifica MCP. https://modelcontextprotocol.io/
- "Specification 2025-03-26" (Streamable HTTP). https://modelcontextprotocol.io/specification/2025-03-26
- "Specification 2025-11-25" (Tasks, elicitation, extensions, authorization). https://modelcontextprotocol.io/specification/2025-11-25
- "One Year of MCP: November 2025 Spec Release". https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/
- Official MCP Registry. https://registry.modelcontextprotocol.io/
- MCP GitHub organization. https://github.com/modelcontextprotocol
- MCP Python SDK. https://github.com/modelcontextprotocol/python-sdk
- "Awesome MCP servers". https://github.com/punkpeye/awesome-mcp-servers
- Google Cloud, "Google-managed MCP servers are available for everyone", maggio 2026. https://cloud.google.com/blog/products/ai-machine-learning/google-managed-mcp-servers-are-available-for-everyone
- Cloudflare, "Why we built remote MCP support", 2025.
- OpenAI, "Agents SDK MCP integration docs". https://platform.openai.com/docs

## Note operative

Versioning. La spec MCP evolve con cadenza rapida. Le release sono identificate da date (es. 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25). Client e server negoziano la versione comune all'`initialize`. La revisione 2025-11-25 e' dichiarata backward compatible: le nuove feature (Tasks, elicitation, sampling con tool, extensions) sono adottabili in modo incrementale. La compatibilita' all'indietro resta non garantita sulle feature ancora sperimentali: aggiornare le librerie SDK e' un'attivita' di manutenzione regolare.

Discovery e marketplace. Oltre ai registry pubblici di terze parti (mcp.so, smithery.ai, glama.ai) esiste ora un registry ufficiale, registry.modelcontextprotocol.io, che funge da indice centrale per la discovery dei server e che a fine maggio 2026 indicizza diverse migliaia di server (dell'ordine di 9.000+ record). La provenance di un server resta un tema di sicurezza: installare un MCP server arbitrario equivale a installare un binario. Le best practice includono code signing, sandboxing del processo (per stdio server) e revocabilita' di credenziali (per remote server). I client maturi (Claude Desktop, Cursor) richiedono conferma esplicita all'utente per ogni nuovo server registrato.

Debugging. MCP introduce un confine di processo che complica il debug: un tool call fallito puo' essere colpa del client, del trasporto, del server, della funzione sottostante. SDK maturi espongono modalita' verbose con dump JSON-RPC, e tool come MCP Inspector permettono di interrogare manualmente un server senza un client AI. Per integrazioni in produzione vale la pena standardizzare structured logging in entrambi i lati.

Pattern di adozione enterprise. Nelle organizzazioni che hanno introdotto MCP nel 2025-2026, lo schema ricorrente e': un team piattaforma costruisce un parco di server MCP interni (CRM, ERP, knowledge base) con autenticazione SSO, e li espone ai team applicativi che li integrano nei propri agenti. Il vantaggio e' che la security review si fa una volta sul server, non per ogni applicazione che lo consuma. Nei settori regolamentati (finanza, healthcare, legal) la combinazione self-hosted sandbox + MCP tunnel risponde ai due blocchi piu' frequenti all'adozione di agenti gestiti: il controllo sui dati e l'esposizione di sistemi interni a internet. Vedi anche [agent-sandboxing](./agent-sandboxing.md) per il modello di containment dell'esecuzione tool.

## Aggiornamenti

### 2026-07-29

Pubblicata il 28 luglio la spec 2026-07-28, la quinta revisione della cronologia e il cambiamento piu' grande da quando MCP remoto e' stato lanciato oltre un anno fa: il nucleo del protocollo passa da bidirezionale/stateful a request/response stateless. Sparisce l'handshake `initialize`/`initialized` con i session ID (`Mcp-Session-Id`), sostituito da Multi Round-Trip Requests per le richieste che il server deve avviare verso il client — la ragione pratica e' che il modello a sessione impediva di eseguire server MCP dietro load balancer o su infrastruttura edge/serverless senza storage condiviso. Arrivano inoltre routing basato su header (`Mcp-Method`, `Mcp-Name`), risultati di lista cacheable (`ttlMs`, `cacheScope`), hardening dell'autorizzazione allineato a OAuth/OIDC (RFC 9207, passaggio da Dynamic Client Registration a Client ID Metadata Documents) e un framework formale di lifecycle delle feature (Active/Deprecated/Removed, minimo 12 mesi tra deprecazione e rimozione) dentro cui Tasks e MCP Apps diventano estensioni versionate ufficiali. SDK Tier 1 (TypeScript, Python, Go, C#) gia' aggiornati, Rust in beta; il blog MCP dichiara quasi 500 milioni di download al mese sugli SDK Tier 1, oltre 1 miliardo cumulati per TS e Python. Anthropic adotta la nuova spec da subito in Claude (dati MCP live per artifact pubblicati, nuove opzioni di condivisione team/enterprise). E' la prima volta che la specifica opera un cambio architetturale del core (stateful -> stateless) invece di aggiungere primitive incrementali come nella revisione 2025-11-25: sposta il baricentro del protocollo dalla ricchezza di feature alla scalabilita' operativa su infrastruttura moderna (edge, serverless, multi-tenant). [Digest 2026-07-29](../../digest/2026/07/29.md)

### 2026-05-29

Google lancia il Google Pay & Wallet Developer MCP Server in Public Preview (28 maggio): un server MCP ufficiale che espone le API di Google Pay e Google Wallet come tool per agenti AI e assistant di sviluppo. Le capability esposte includono ricerca nella documentazione ufficiale, gestione delle integrazioni, accesso a metriche e log, gestione dei pass emitters per Google Wallet. Contestualmente Google ha reso disponibili MCP server gestiti per altre API cloud ("Google-managed MCP servers are available for everyone"). Il lancio segnala che Google adotta MCP come interfaccia standard per esporre servizi production-grade ad agenti — lo stesso passaggio che ha portato OpenAI ad aggiungere il supporto MCP ad Agents SDK e ChatGPT Desktop. Il pattern convergente dei tre grandi lab (Anthropic, OpenAI, Google) verso MCP come strato di interoperabilita' conferma che il protocollo si e' affermato come standard de facto. [Digest 2026-05-29](../../digest/2026/05/29.md)

### 2026-05-31

Anthropic pubblica il post di ingegneria "How we contain Claude across products" (30 maggio), che include la prima documentazione tecnica pubblica dei MCP tunnels nell'architettura di sicurezza enterprise di Claude. I MCP tunnels (research preview da maggio 2026) permettono agli agenti Claude di raggiungere MCP server nella rete privata aziendale attraverso un gateway outbound-only: nessuna regola di firewall inbound, nessun endpoint pubblico esposto, traffico cifrato end-to-end. Questo pattern — gia' descritto funzionalmente nel digest 05-28 per il lancio di Claude Managed Agents — riceve ora una collocazione precisa nell'architettura di containment: i MCP tunnels sono lo strato di connettivita' che permette all'agente (loop su Anthropic) di usare tool interni aziendali (MCP server in rete privata) senza che i dati aziendali escano dal perimetro. La documentazione fornisce ai security architect il modello di minaccia preciso: cosa puo' raggiungere un agente compromesso in ogni configurazione, e quali controlli tecnologici limitano l'esposizione. [Digest 2026-05-31](../../digest/2026/05/31.md)

### 2026-06-01

Nel mese di maggio 2026 il segnale dominante e' il consolidamento di MCP come standard di interoperabilita' adottato strutturalmente dai grandi lab, con un baricentro che si sposta dal "come si scrive un server" al "come si distribuiscono, governano e mettono in sicurezza i server in produzione". Tre cluster di novita' verificabili nei digest del mese.

Primo, i vendor-managed server: Google lancia il Google Pay & Wallet Developer MCP Server e rende disponibili MCP server gestiti per le proprie API cloud ([digest 05-29](../../digest/2026/05/29.md)); a inizio mese Anthropic aveva introdotto il MCP connector Moody's (dati su 600+ milioni di aziende) nei suoi agenti per i financial services ([digest 05-07](../../digest/2026/05/07.md)) e, con Thomson Reuters, un connettore MCP verso Westlaw/Practical Law/KeyCite per CoCounsel ([digest 05-13](../../digest/2026/05/13.md)). Il provider del servizio pubblica e mantiene direttamente il server ufficiale: gli sviluppatori smettono di costruire wrapper manuali sulle API REST.

Secondo, la sicurezza del deployment enterprise: Claude Managed Agents introduce self-hosted sandboxes (public beta) e MCP tunnels (research preview) per tenere il loop agentico sul provider e l'esecuzione tool piu' i dati nel perimetro del cliente ([digest 05-28](../../digest/2026/05/28.md)); il post di ingegneria "How we contain Claude" colloca i MCP tunnels nell'architettura di containment complessiva e fornisce il modello di minaccia ([digest 05-31](../../digest/2026/05/31.md)). Claude Platform on AWS espone il connettore MCP in beta tra le sue feature native ([digest 05-13](../../digest/2026/05/13.md)).

Terzo, la toolchain: l'acquisizione di Stainless da parte di Anthropic ([digest 05-19](../../digest/2026/05/19.md), [digest 05-27](../../digest/2026/05/27.md)) porta in casa l'infrastruttura che generava automaticamente SDK e MCP server da OpenAPI per OpenAI, Google e Cloudflare — un segnale del valore strategico attribuito al layer di generazione MCP.

Sul piano della specifica, oltre alle novita' viste nei digest, vale la pena registrare la maturazione del protocollo intervenuta nel novembre 2025 (primo anniversario): la revisione 2025-11-25 ha introdotto i Tasks asincroni ("call-now, fetch-later"), la URL Mode Elicitation (SEP-1036), il Sampling con tool (SEP-1577), l'Extensions framework e le Authorization Extensions (OAuth client-credentials, SEP-1046), in modo backward compatible. E' inoltre operativo il registry ufficiale registry.modelcontextprotocol.io, che a fine maggio 2026 indicizza dell'ordine di 9.000+ server. La scheda e' stata riscritta in profondita': aggiunte le sezioni su Tasks/elicitation/sampling-con-tool nel "Come funziona", il pattern vendor-managed server in "Varianti", l'esempio asincrono e l'esempio con MCP tunnel in "Esempi pratici", e aggiornate le note operative su versioning e registry. Fonti spec verificate: blog.modelcontextprotocol.io e modelcontextprotocol.io.
