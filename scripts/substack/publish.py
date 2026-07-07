#!/usr/bin/env python3
"""Publisher Fase 2: crea BOZZE Substack dai pacchetti prodotti da convert.py.

Usa la libreria non ufficiale python-substack (API interne, autenticazione via
cookie di sessione). NON pubblica: crea solo draft only_paid nella Section
"Fondamenti di AI"; la pubblicazione resta un'azione manuale dell'autrice.

Prerequisiti:
  1. python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
  2. Creare la Section "Fondamenti di AI" su Substack (Settings > Sections).
  3. Copiare config.example.json in .secrets/config.json e inserire il cookie
     di sessione (connect.sid[; substack.sid]) del proprio account.

Uso:
  python3 publish.py            # solo il pilota (capitolo 01)
  python3 publish.py all        # tutti i 28 capitoli
  python3 publish.py 03         # solo il capitolo 03
"""
import glob
import json
import os
import struct
import sys

try:
    from substack import Api
    from substack.post import Post
    from substack.exceptions import SubstackAPIException
except ImportError:
    sys.exit("python-substack non installato. Esegui: .venv/bin/pip install -r requirements.txt")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SECRETS = os.path.join(HERE, ".secrets", "config.json")
SECTION_NAME = "Fondamenti di AI"


def load_config():
    if not os.path.exists(SECRETS):
        sys.exit(
            f"Config mancante: {SECRETS}\n"
            "Copia config.example.json in .secrets/config.json e inserisci "
            "il cookie di sessione Substack (connect.sid).")
    cfg = json.load(open(SECRETS, encoding="utf-8"))
    if not cfg.get("publication_url"):
        sys.exit("config.json: 'publication_url' mancante.")
    if not (cfg.get("cookies_string") or (cfg.get("email") and cfg.get("password"))):
        sys.exit("config.json: fornisci 'cookies_string' oppure 'email'+'password'.")
    return cfg


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def runs_to_chunks(runs):
    """runs {text,marks} -> chunk {content,marks} attesi da add_complex_text."""
    return [{"content": r["text"], "marks": r.get("marks", [])} for r in runs]


def runs_to_prosemirror(runs):
    """runs -> nodi text ProseMirror grezzi (per le liste, non coperte dal builder)."""
    nodes = []
    for r in runs:
        marks = []
        for m in r.get("marks", []):
            if m["type"] == "link":
                marks.append({"type": "link", "attrs": {"href": m["href"]}})
            else:
                marks.append({"type": m["type"]})
        node = {"type": "text", "text": r["text"]}
        if marks:
            node["marks"] = marks
        nodes.append(node)
    return nodes


def upload_image_url(api, path):
    resp = api.get_image(path)
    if isinstance(resp, str):
        return resp
    return resp.get("url") or resp.get("src") or resp.get("imageUrl")


def build_post(api, user_id, sections, data, base_dir):
    post = Post(data["title"], data.get("subtitle", ""), user_id, audience=data.get("audience", "only_paid"))
    post.set_section(SECTION_NAME, sections)

    for b in data["blocks"]:
        if b["type"] == "heading":
            post.add({"type": "heading", "level": 2, "content": runs_to_chunks(b["runs"])})
        elif b["type"] == "paragraph":
            post.add({"type": "paragraph", "content": runs_to_chunks(b["runs"])})
        elif b["type"] == "list":
            items = [
                {"type": "listItem",
                 "content": [{"type": "paragraph", "content": runs_to_prosemirror(it)}]}
                for it in b["items"]
            ]
            post.draft_body["content"].append({"type": "bulletList", "content": items})
        elif b["type"] == "image":
            fig = b["figure"]
            path = os.path.join(base_dir, "images", fig["file"])
            url = upload_image_url(api, path)
            w, h = png_size(path)
            post.add({"type": "captionedImage", "src": url, "alt": fig.get("alt", ""),
                      "width": w, "height": h, "resizeWidth": 728})
            if fig.get("caption"):
                post.add({"type": "paragraph",
                          "content": [{"content": fig["caption"], "marks": [{"type": "em"}]}]})
    return post


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "01"
    cfg = load_config()
    api = Api(
        email=cfg.get("email"), password=cfg.get("password"),
        cookies_string=cfg.get("cookies_string"),
        publication_url=cfg["publication_url"],
    )
    user_id = api.get_user_id()
    sections = api.get_sections()
    if not any(s.get("name") == SECTION_NAME for s in sections):
        names = ", ".join(s.get("name", "?") for s in sections) or "(nessuna)"
        sys.exit(f"Section '{SECTION_NAME}' non trovata. Sezioni esistenti: {names}\n"
                 "Creala su Substack (Settings > Sections) e riprova.")

    dirs = sorted(glob.glob(os.path.join(OUT, "*", "post.json")))
    if arg != "all":
        dirs = [p for p in dirs if os.path.basename(os.path.dirname(p)).startswith(arg)]
    if not dirs:
        sys.exit(f"Nessun pacchetto per '{arg}'. Esegui prima: python3 convert.py")

    print(f"Publisher: {len(dirs)} capitolo/i, Section '{SECTION_NAME}', solo BOZZE (only_paid).")
    for pj in dirs:
        base_dir = os.path.dirname(pj)
        data = json.load(open(pj, encoding="utf-8"))
        try:
            post = build_post(api, user_id, sections, data, base_dir)
            resp = api.post_draft(post.get_draft())
        except SubstackAPIException as e:
            print(f"  ERRORE cap {data['chapter']:>2} {data['title'][:30]}: {e}")
            continue
        draft_id = resp.get("id")
        print(f"  OK bozza cap {data['chapter']:>2}  {data['title'][:34]:<34}  draft_id={draft_id}")
    print("Fatto. Rivedi le bozze su Substack e pubblica manualmente.")


if __name__ == "__main__":
    main()
