# Pipeline Fondamenti → Substack

Porta i 28 capitoli di [`fondamenti/`](../../fondamenti) sulla newsletter Substack
[*Minimum Viable Knowledge*](https://giadaf.substack.com/) come serie a pagamento
"Fondamenti di AI".

**Perché serve una pipeline.** Substack non ha API pubblica di scrittura (il
Developer API 2025 è di sola lettura) e non importa Markdown né SVG. Quindi:
il contenuto va convertito in blocchi ProseMirror e i diagrammi rasterizzati in PNG.

**Nota ToS.** La Fase 2 usa la libreria non ufficiale `python-substack`, che chiama
le API interne di Substack autenticandosi con un cookie di sessione. È una zona grigia
sui Termini di Servizio. Per ridurre il rischio la pipeline crea **solo bozze**
(`only_paid`): la pubblicazione resta un'azione manuale. Il cookie è una credenziale
sensibile (accesso totale all'account): vive solo in `.secrets/` (gitignored), mai committato.

## Fase 1 — Conversione (nessuna credenziale)

```bash
python3 convert.py          # tutti i 28 capitoli
python3 convert.py 01       # solo il pilota
```

Per ogni capitolo produce `out/NN-<slug>/`:
- `post.json` — titolo, sottotitolo, `audience=only_paid`, section, blocchi (heading/
  paragrafi/liste/immagini) con link già riscritti in assoluti verso aideepdive.vercel.app
  e attribuzione in coda;
- `images/figK.png` — i diagrammi SVG rasterizzati (rsvg-convert, CSS tema chiaro
  iniettato, sfondo bianco, 2x);
- `preview.html` — anteprima renderizzata: **aprila nel browser per il controllo visivo**.

Dipendenza di sistema: `rsvg-convert` (librsvg). `out/` è rigenerabile e gitignored.

## Fase 2 — Bozze su Substack (richiede accesso)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

1. **Crea la Section** "Fondamenti di AI" su Substack: Settings → Sections → New section.
2. **Estrai il cookie di sessione** (metodo più affidabile — prende tutti i cookie giusti,
   `substack.sid` incluso): fai login su substack.com, apri DevTools (F12) → tab **Network** →
   clicca una qualsiasi richiesta a `substack.com` → sezione **Request Headers** → copia
   l'**intero valore** dell'header `Cookie:` (una stringa lunga tipo `ajs_anonymous_id=...;
   substack.sid=...; connect.sid=...`).
3. **Configura** (file gitignored):
   ```bash
   mkdir -p .secrets && cp config.example.json .secrets/config.json
   # incolla la stringa Cookie in "cookies_string" dentro .secrets/config.json
   ```
4. **Crea le bozze**:
   ```bash
   .venv/bin/python publish.py          # solo il pilota (cap. 01)
   .venv/bin/python publish.py all      # tutti i 28
   .venv/bin/python publish.py 03       # un capitolo specifico
   ```
   Lo script carica i PNG, costruisce il corpo, imposta `only_paid` + Section, e crea
   le **bozze**. Non pubblica nulla.
5. **Rivedi e pubblica** ogni bozza dall'editor Substack.

Il cookie scade dopo settimane/mesi: se `publish.py` dà errori di autenticazione,
rigeneralo (punto 2) e riaggiorna `.secrets/config.json`.
