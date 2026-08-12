---
name: Watermarking
aliases: [watermarking, filigrana digitale, AI text watermarking, digital watermarking, content provenance, provenienza dei contenuti, C2PA]
categoria: tecnica
created: 2026-08-12
last_updated: 2026-08-12
---

# Watermarking

## Cos'e

Il watermarking (filigrana digitale) applicato ai modelli generativi e' l'insieme di tecniche che incorporano, nel contenuto prodotto da un [LLM](./llm.md) o da un modello generativo affine, un segnale statistico o crittografico invisibile a occhio nudo ma rilevabile con uno strumento dedicato, allo scopo di attribuire quel contenuto alla propria origine artificiale. A differenza di una filigrana visibile su un'immagine (un logo semitrasparente), il watermarking di cui si parla nel 2026 per testo, immagini, audio e video generati da AI e' pensato per non alterare percettibilmente il contenuto: un lettore umano non nota nulla di diverso, ma un classificatore o un test statistico dedicato puo' confermare con alta probabilita' se quel testo o quell'immagine e' passato attraverso un determinato modello.

Il tema e' diventato rilevante su scala industriale nel 2026 per la convergenza di tre pressioni distinte. La prima e' regolatoria: l'AI Act dell'Unione Europea impone, tramite il proprio Transparency Code (obbligo gia' in vigore dal 2 agosto 2025, con enforcement e sanzioni attive dal 2 agosto 2026, vedi [ai-governance.md](./ai-governance.md)), la marcatura leggibile da macchina dei contenuti generati da AI e l'etichettatura dei deepfake. La seconda e' di fiducia pubblica: con l'aumento del volume di testo, immagini e video sintetici in circolazione, distinguere contenuto umano da contenuto generato diventa un problema di integrita' dell'informazione (disinformazione, plagio accademico, contraffazione di prove). La terza e' competitiva: un laboratorio che dimostra di poter tracciare l'origine dei propri output puo' usarlo come argomento di responsabilita' e differenziazione rispetto a concorrenti che non lo fanno.

L'11 agosto 2026 Anthropic annuncia che tutti i modelli Claude rilasciati dal 2 agosto 2026 incorporano un watermark statistico invisibile nel testo generato, attivo di default su ogni superficie del prodotto — Claude Platform API, claude.ai, Claude Code, Claude Cowork, Claude Tag, e i deployment Claude su AWS, Google Cloud e Microsoft Foundry — e dichiara di lavorare all'estensione ai modelli precedenti. E' il primo impegno esplicito e globale (non limitato agli utenti europei, pur rispondendo in parte al Transparency Code UE) da parte di un laboratorio frontier occidentale a marcare in modo sistematico e verificabile l'origine del proprio output testuale.

## Come funziona

Il problema tecnico del watermarking testuale e' diverso da quello del watermarking su immagini o audio, perche' il testo e' un segnale discreto a bassissima ridondanza: non esistono "pixel di scarto" in cui nascondere un bit senza rischiare di alterare il significato o la naturalezza della frase. Le famiglie di tecniche pubblicamente note nella letteratura di ricerca — usate come riferimento generale del campo, indipendentemente dai dettagli implementativi specifici che i singoli laboratori scelgono di non divulgare — si dividono in due approcci principali.

**Watermarking a livello di generazione (green-red list).** L'approccio piu' citato in letteratura, proposto da Kirchenbauer et al. nel 2023, agisce durante il campionamento del token successivo. Prima di scegliere il token, un hash pseudo-casuale calcolato a partire dal contesto recente (gli ultimi n token gia' generati) divide l'intero vocabolario in due insiemi: una "green list" di token favoriti e una "red list" di token penalizzati. Il modello applica un piccolo bias positivo ai logit dei token nella green list prima di campionare, cosi' che nel testo finale i token della green list compaiono in proporzione statisticamente superiore al caso, senza che il bias sia percepibile a un lettore umano su un singolo testo. Chi possiede la chiave dell'hash (tipicamente solo il laboratorio che ha generato il testo) puo' rifare il calcolo della green/red list per ogni posizione e contare quanti token osservati cadono nella green list: uno z-test statistico stabilisce se lo scarto rispetto al 50% atteso da un testo non marcato e' significativo, restituendo un punteggio di confidenza (non un verdetto binario) che il testo sia stato generato da quel modello.

**Watermarking a livello di campionamento crittografico.** Una seconda famiglia, associata al lavoro di Scott Aaronson (consulente per OpenAI su questo tema nel 2022-2023), usa una funzione pseudo-casuale crittografica per guidare l'intero processo di campionamento (non solo il bias sui logit) in modo che la sequenza di scelte del modello sia deterministicamente riconducibile a un seed segreto, pur restando statisticamente indistinguibile da un campionamento normale per chi non conosce il seed. Questo approccio tende a preservare meglio la qualita' del testo a parita' di rilevabilita', a costo di una maggiore complessita' implementativa.

**Watermarking su immagini e audio.** Per contenuti continui (pixel, campioni audio) la marcatura opera tipicamente nel dominio della frequenza o nello spazio latente del modello di diffusione, inserendo un pattern impercettibile ma statisticamente rilevabile che sopravvive a ricompressione e ridimensionamento moderati. SynthID di Google DeepMind, pubblicato in ricerca su Nature nell'ottobre 2024 ed esteso a testo, immagini, audio e video nel corso del 2025-2026, e' il riferimento pubblico piu' documentato di questa famiglia integrata multi-modale.

**Provenienza tramite metadata: C2PA.** Distinto dal watermarking statistico "nascosto nel contenuto", lo standard C2PA (Coalition for Content Provenance and Authenticity, promosso da Adobe, Microsoft, Intel, BBC e altri) allega ai file (immagini, video, PDF) metadata firmati crittograficamente che dichiarano esplicitamente la catena di provenienza — quale strumento ha creato o modificato il file, e quando. A differenza del watermark statistico, il metadata C2PA e' visibile e verificabile da chiunque abbia accesso al file originale, ma viene perso se il file viene ri-esportato, screenshottato o convertito in un formato che non lo preserva. Anthropic dichiara di adottare lo standard C2PA per i file generati da Claude, in aggiunta al watermark statistico invisibile per il testo.

## Varianti / approcci

**Robustezza vs. impercettibilita'.** Ogni schema di watermarking testuale bilancia due obiettivi in tensione: un bias piu' forte sui token della green list rende il segnale piu' facile da rilevare anche su testi brevi, ma aumenta il rischio che il testo suoni innaturale o che la scelta lessicale del modello venga distorta in modo percepibile. Anthropic dichiara che il proprio watermark sopravvive al copia-incolla (il caso d'uso piu' comune: un utente copia l'output di Claude in un altro documento) e resta parzialmente rilevabile dopo editing leggero, ma si degrada con parafrasi pesante o traduzione — un limite strutturale comune a tutti gli schemi statistici noti: riscrivere il testo con parole proprie, anche mantenendo lo stesso significato, cambia la sequenza di token e quindi il pattern statistico rilevabile.

**Watermarking invisibile vs. disclosure esplicita.** Il watermarking statistico coesiste, senza sostituirla, con la disclosure esplicita — un banner "generato da AI", una dicitura nei metadata visibili, un footer testuale. L'AI Act UE richiede entrambe le cose a seconda del contesto: disclosure sui chatbot (l'utente deve sapere che sta parlando con un'AI) e marcatura machine-readable dei contenuti generati (che puo' essere invisibile all'utente finale ma leggibile da strumenti automatici). Il watermarking invisibile serve principalmente il secondo obiettivo: permette a piattaforme terze, motori di ricerca o strumenti di fact-checking di verificare automaticamente l'origine di un contenuto senza dover fidarsi di una dichiarazione volontaria dell'utente che lo ripubblica.

**Watermarking a livello di modello vs. a livello di prodotto.** Una distinzione operativa rilevante per chi valuta l'affidabilita' di uno schema: un watermark applicato a livello di modello (come nel caso Claude, dove Anthropic dichiara che il segnale e' incorporato nel processo di generazione stesso) e' presente su ogni canale attraverso cui il modello viene servito, incluse le integrazioni di terze parti che usano la stessa API. Un watermark applicato a livello di prodotto (ad esempio solo nell'interfaccia web ufficiale) puo' essere aggirato semplicemente accedendo al modello tramite un canale diverso (API diretta, self-hosting per i modelli open-weight). La scelta di Anthropic di applicare il watermark su tutte le superfici, incluse le piattaforme cloud partner, e' coerente con un watermark a livello di modello piuttosto che di singola interfaccia.

**Watermark rimovibile per design vs. resistente ad attacco.** Nessuno schema di watermarking testuale pubblicamente noto e' resistente a un attaccante motivato che riscrive deliberatamente il testo con un altro modello (watermark laundering) o applica tecniche di parafrasi automatica pensate specificamente per rompere il pattern statistico. La letteratura di ricerca tratta questo come un problema aperto: il watermarking testuale offre evidenza probabilistica utile in scenari di uso ordinario (individuare testo non modificato o solo leggermente editato), non una garanzia crittografica contro un avversario che investe risorse per rimuoverlo.

## Quando usarlo

**Ha senso adottarlo quando:**
- Si e' un laboratorio o piattaforma che genera contenuto su larga scala e si vuole offrire uno strumento di verifica dell'origine a terzi (piattaforme social, motori di ricerca, redazioni) senza dover esporre dati sugli utenti.
- Si opera in una giurisdizione con obblighi di marcatura machine-readable dei contenuti generati da AI (AI Act UE, e normative analoghe in discussione altrove).
- Si vuole un meccanismo di attribuzione che non richieda cooperazione dell'utente (a differenza di una dicitura volontaria, che l'utente puo' rimuovere semplicemente non includendola quando ripubblica il testo).
- Il caso d'uso prevalente e' la verifica su testo non pesantemente modificato: rilevare se un compito scolastico, un articolo o un post e' stato generato integralmente da AI con editing minimo.

**E' meno efficace o non sufficiente quando:**
- Il testo viene tradotto, parafrasato pesantemente o riscritto da un secondo modello prima della pubblicazione: il segnale statistico si degrada in modo sostanziale.
- Serve una prova legale o forense a prova di contestazione: il watermarking statistico fornisce un punteggio di confidenza probabilistico, non un verdetto binario certo, ed e' verificabile solo da chi detiene la chiave (tipicamente il laboratorio stesso), il che introduce un problema di fiducia nella terza parte che esegue la verifica.
- Il modello e' open-weight e self-hosted: un utente che esegue il modello sulla propria infrastruttura puo' in teoria disabilitare o modificare il meccanismo di watermarking se questo e' implementato nel codice di inferenza pubblico, a differenza di un modello servito esclusivamente via API chiusa.
- Si vuole prevenire, non solo rilevare, l'uso malevolo di contenuto generato: il watermarking e' uno strumento di attribuzione post-hoc, non un blocco preventivo alla generazione di contenuto dannoso (quel problema appartiene piuttosto ai classificatori di safety e ai guardrail di [agent sandboxing](./agent-sandboxing.md) per gli output eseguibili).

## Esempi pratici

**Verifica editoriale.** Una redazione riceve un testo sospettato di essere generato da AI e lo sottopone allo strumento di verifica del laboratorio (dove disponibile pubblicamente): il risultato e' un punteggio di confidenza, non una certezza, e va trattato come indizio da incrociare con altre verifiche editoriali, non come prova definitiva.

**Piattaforma di pubblicazione.** Un social network o un aggregatore di contenuti integra la verifica del watermark nel proprio pipeline di moderazione per etichettare automaticamente i post generati da AI non dichiarati come tali, riducendo il carico sui moderatori umani per i casi piu' evidenti.

**Compliance normativa.** Un'azienda che usa Claude per generare contenuto destinato al mercato europeo si affida al watermark nativo del modello per soddisfare l'obbligo di marcatura machine-readable dell'AI Act, senza dover implementare un proprio sistema di etichettatura separato.

**Limite pratico osservato al lancio.** Al momento dell'annuncio dell'11 agosto, diversi commentatori tecnici hanno sollevato dubbi sulla robustezza pratica del meccanismo in scenari di uso comune (copia-incolla parziale, riscrittura leggera, traduzione), riflettendo il limite strutturale gia' noto in letteratura: il watermarking statistico funziona meglio come deterrente e strumento di attribuzione probabilistica su larga scala che come garanzia puntuale su un singolo testo fortemente modificato.

## Letture

- Kirchenbauer, Geiping, Wen et al., "A Watermark for Large Language Models", 2023. https://arxiv.org/abs/2301.10226
- Dathathri et al. (Google DeepMind), "Scalable watermarking for identifying large language model outputs" (SynthID-Text), Nature, 2024. https://www.nature.com/articles/s41586-024-08025-4
- Coalition for Content Provenance and Authenticity (C2PA), specifica tecnica. https://c2pa.org/specifications/specifications/2.1/index.html
- TechCrunch — "Anthropic says it will watermark text generated by its AI models", 11 agosto 2026. https://techcrunch.com/2026/08/11/anthropic-says-it-will-watermark-text-generated-by-its-ai-models/

## Aggiornamenti

### 2026-08-12

Prima menzione nel digest: Anthropic annuncia l'11 agosto 2026 un watermark statistico invisibile attivo su tutti i modelli Claude rilasciati dal 2 agosto 2026, su ogni superficie di prodotto, con adozione dello standard C2PA per i file generati. [Digest 2026-08-12](../../digest/2026/08/12.md)
