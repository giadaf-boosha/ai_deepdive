---
name: Model Context Protocol
aliases: [MCP, Model Context Protocol, protocollo MCP]
categoria: infrastruttura
created: 2026-04-28
last_updated: 2026-04-28
mentions_count: 0
---

# Model Context Protocol

## Cos'e

Model Context Protocol (MCP) e' un protocollo aperto, basato su JSON-RPC 2.0, che standardizza il modo in cui le applicazioni AI espongono e consumano contesto: tool, dati, prompt template, accesso a sistemi esterni. E' stato pubblicato da Anthropic nel novembre 2024 come specifica open source con SDK in TypeScript, Python, Go, Java, Rust. L'analogia ricorrente e' "USB-C per gli LLM": un'interfaccia uniforme tra modello e mondo, che sostituisce le integrazioni N x M (N modelli x M tool) con N + M.

Il problema che MCP risolve nasce dalla diffusione del [tool use](./tool-use.md) negli [agent](./agent.md). Prima di MCP, ogni framework aveva il proprio formato di descrizione tool, ogni applicazione integrava sistemi esterni con codice ad-hoc, ogni connettore Slack o GitHub veniva riscritto in dozzine di repository. MCP definisce un'API neutrale: un MCP server espone capacita' (tools, resources, prompts), un MCP client (un'app come Claude Desktop, Cursor, un agent SDK) le consuma. La stessa configurazione di server funziona con qualunque modello e qualunque client conforme.

L'adozione e' stata rapida. Tra il 2024 e il 2026 OpenAI ha aggiunto supporto MCP in ChatGPT desktop e Agents SDK; Google nel Gemini SDK; IDE come Cursor, Windsurf, JetBrains, VS Code lo supportano nativamente; sono nati registry pubblici (mcp.so, smithery.ai) con migliaia di server. MCP e' diventato lo strato di interoperabilita' di fatto per agenti, in modo analogo a come HTTP lo e' per il web e LSP per gli editor di codice.

## Come funziona

MCP definisce due ruoli e tre primitive principali. I ruoli sono client (l'app AI o l'agente) e server (espone capacita'). Le primitive sono:

Tools. Funzioni invocabili dal modello. Hanno nome, descrizione, input schema (JSON Schema), e ritornano contenuto (testo, immagine, embedded resource). Esempio: `create_issue(repo, title, body)` esposto da un GitHub MCP server. Il modello vede la descrizione e decide quando chiamare il tool; il client esegue la chiamata RPC al server e restituisce il risultato al modello.

Resources. Dati indirizzabili con URI (`file://`, `postgres://`, `slack://channel/123`). Sono passivi: il server li espone, il client li include nel contesto su richiesta dell'utente o dell'app. Servono per dare al modello accesso a documenti, query di database, log, senza che il modello debba "chiamarli". La distinzione tools vs resources e' application-controlled vs user-controlled: i tool sono decisi dal modello, le resource selezionate dall'utente o dall'app.

Prompts. Template di prompt parametrizzati che l'utente puo' invocare come slash command. Servono per workflow ripetibili (es. `/code-review pr_url`) standardizzati tra applicazioni.

Trasporto. MCP supporta tre trasporti. Stdio: il server gira come processo locale, comunicazione su stdin/stdout. Adatto a tool che girano sulla macchina dell'utente (filesystem, git, bash). Streamable HTTP: il server e' un endpoint HTTP che supporta long-running streams via Server-Sent Events. Adatto a server remoti, multi-tenant, deployabili come microservizi. (Una versione precedente "HTTP+SSE" e' stata rimpiazzata da Streamable HTTP nella spec 2025-03-26.) WebSocket: meno usato, supportato in alcuni SDK.

Lifecycle. Il client all'avvio invia `initialize` dichiarando capacita' supportate (sampling, roots) e versione protocollo; il server risponde con le proprie capacita' e l'elenco di tools, resources, prompts. Da quel momento il client puo' inviare `tools/list`, `tools/call`, `resources/read`, `prompts/get`. Il server puo' anche inviare richieste sampling al client (chiedere al modello di fare una chiamata LLM, lasciando il modello e i token al client).

Sicurezza. La spec impone consenso esplicito dell'utente per tool execution, per resource exposure, per sampling. Le applicazioni client devono mostrare quale server sta eseguendo cosa. La superficie d'attacco principale (prompt injection da contenuto restituito dai tool, server malevoli che esfiltrano dati) e' coperta da raccomandazioni operative: sandbox dei server, audit log, allowlist.

## Varianti / approcci

MCP non ha "varianti" in senso architetturale ma ha pattern di deployment differenti.

| Pattern | Trasporto | Uso |
|---|---|---|
| Local-first server | stdio | Tool che operano su file locali, repo, container dell'utente |
| Remote SaaS server | streamable HTTP | Integrazioni con servizi cloud (Slack, Notion, Linear, GitHub) |
| Internal enterprise server | HTTP, autenticato | Strumenti aziendali (CRM, ERP, datawarehouse) |
| Marketplace server | HTTP, multi-tenant | Server condivisi pubblicati su registry |

Confronto con alternative.

| Approccio | Pro | Contro |
|---|---|---|
| MCP | Standard aperto, ecosistema crescente, neutralita' | Overhead di setup, stato in evoluzione |
| Function calling proprietario (OpenAI tools, Anthropic tools) | Semplice, integrato | Vendor lock-in, non interoperabile |
| Plugin proprietari (es. ChatGPT plugins, dismessi) | UX integrata | Ecosistema chiuso, deprecato |
| OpenAPI / REST diretto | Standard maturo | Manca contratto pensato per LLM (descrizioni semantiche) |
| LangChain Tools | Ricco, Python-first | Lock-in al framework |

Una scelta progettuale tipica e' usare MCP per i tool di sistema/dominio e mantenere il function calling nativo per tool ad-hoc tightly coupled all'app.

## Quando usarlo / quando no

MCP e' la scelta giusta quando si costruisce un agente che integra molti tool eterogenei, quando si vuole esporre capacita' a piu' modelli/client senza riscrivere codice, quando l'organizzazione vuole un layer di tool centralizzato e auditabile, quando si lavora su un IDE o desktop client che gia' supporta MCP. Esempi: agenti di coding che usano filesystem + git + bash + linguaggi-specifici; assistenti aziendali che orchestrano Slack, Linear, Notion; strumenti di data analytics che combinano database + filesystem + LLM.

MCP e' la scelta sbagliata quando si fa una singola chiamata LLM con un solo tool deterministico (overkill), quando la latenza extra del trasporto e' inaccettabile (microsecond budget), quando il tool e' un dettaglio interno dell'app e non andra' mai esposto altrove, quando si lavora in un ambiente che non supporta i client MCP.

Anti-pattern. Esporre 100+ tool indiscriminatamente: il modello sceglie peggio. Server senza autenticazione su rete pubblica: rischio sicurezza. Confondere tool e resource (mettere tutto come tool spinge l'agente a "cercare" dati che dovrebbero essere passivi). Reinventare descrizioni: la qualita' del campo `description` e dello schema input determina la qualita' delle chiamate del modello.

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

Esempio 2: server remoto enterprise. Un MCP server espone tool `query_warehouse(sql)` autenticato con OAuth2 su HTTPS. L'agente di un analista invoca il tool, riceve dati tabellari, li sintetizza. La governance dell'azienda controlla policy SQL (deny su DROP, rate limiting per utente) lato server, indipendentemente dal client AI.

Esempio 3: combinazione tools + resources. Un MCP server di un repository git espone come resources i file (`file://path`) e come tools `git_diff`, `git_log`, `git_blame`. L'utente puo' aggiungere file specifici al contesto via resource (mostra; il modello li legge), il modello puo' chiamare i tool quando serve aggregazione storica. Questo separa input deliberato (l'utente sceglie cosa mettere in contesto) da azione autonoma (l'agente decide cosa interrogare).

## Letture

- Anthropic, "Introducing the Model Context Protocol", novembre 2024. https://www.anthropic.com/news/model-context-protocol
- Specifica MCP. https://modelcontextprotocol.io/
- MCP GitHub organization. https://github.com/modelcontextprotocol
- "Specification 2025-03-26" (Streamable HTTP). https://modelcontextprotocol.io/specification/2025-03-26
- MCP Python SDK. https://github.com/modelcontextprotocol/python-sdk
- "Awesome MCP servers". https://github.com/punkpeye/awesome-mcp-servers
- Cloudflare, "Why we built remote MCP support", 2025.
- OpenAI, "Agents SDK MCP integration docs". https://platform.openai.com/docs

## Note operative

Versioning. La spec MCP evolve con cadenza rapida. Le release sono identificate da date (es. 2024-11-05, 2025-03-26, 2025-06-18). Client e server negoziano la versione comune all'`initialize`. La compatibilita' all'indietro non e' garantita su feature sperimentali (sampling, roots, elicitation): aggiornare le librerie SDK e' un'attivita' di manutenzione regolare.

Discovery e marketplace. Sono nati registry pubblici dove i server MCP possono essere pubblicati e cercati: mcp.so, smithery.ai, glama.ai. La provenance di un server e' un tema di sicurezza: installare un MCP server arbitrario equivale a installare un binario. Le best practice includono code signing, sandboxing del processo (per stdio server) e revocabilita' di credenziali (per remote server). I client maturi (Claude Desktop, Cursor) richiedono conferma esplicita all'utente per ogni nuovo server registrato.

Debugging. MCP introduce un confine di processo che complica il debug: un tool call fallito puo' essere colpa del client, del trasporto, del server, della funzione sottostante. SDK maturi espongono modalita' verbose con dump JSON-RPC, e tool come MCP Inspector permettono di interrogare manualmente un server senza un client AI. Per integrazioni in produzione vale la pena standardizzare structured logging in entrambi i lati.

Pattern di adozione enterprise. Nelle organizzazioni che hanno introdotto MCP nel 2025, lo schema ricorrente e': un team piattaforma costruisce un parco di server MCP interni (CRM, ERP, knowledge base) con autenticazione SSO, e li espone ai team applicativi che li integrano nei propri agenti. Il vantaggio e' che la security review si fa una volta sul server, non per ogni applicazione che lo consuma.

## Aggiornamenti

Nessun aggiornamento dopo la creazione (2026-04-28).
