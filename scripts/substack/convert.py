#!/usr/bin/env python3
"""Convertitore capitoli Fondamenti (repo markdown) -> pacchetto pubblicabile su Substack.

Per ogni file fondamenti/NN-<slug>.md produce in scripts/substack/out/NN-<slug>/:
  - post.json     struttura del post (titolo, sottotitolo, blocchi, immagini, attribuzione)
  - images/figK.png  diagrammi SVG rasterizzati (rsvg-convert, tema chiaro, sfondo bianco)
  - preview.html  anteprima renderizzata per controllo visivo

Substack non importa Markdown ne SVG: il publisher (Fase 2, python-substack) mappa
post.json sul builder ProseMirror e carica i PNG come asset.

Uso:
  python3 scripts/substack/convert.py            # tutti i capitoli
  python3 scripts/substack/convert.py 01         # solo il capitolo 01 (pilota)
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONDAMENTI = os.path.join(ROOT, "fondamenti")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
SITE = "https://aideepdive.vercel.app"

ATTRIBUTION = (
    "Sintesi originale in italiano. Opera di riferimento: Stuart J. Russell, "
    "Peter Norvig, Intelligenza Artificiale: Un Approccio Moderno, 4a edizione, "
    "Pearson Italia (Vol. 1, 2021; Vol. 2, 2022)."
)

# CSS dei diagrammi con le variabili del tema chiaro risolte a valori concreti
# (da web/app/globals.css). color-mix precalcolato: primary 12% su bianco -> #eee6fc,
# accent 14% su bianco -> #fcefde. rsvg-convert non risolve var()/color-mix.
DIAGRAM_CSS = """
text { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; }
.dg-node { fill:#f1f1f0; stroke:#e2e1e4; stroke-width:1; }
.dg-node-primary { fill:#eee6fc; stroke:#7531e3; stroke-width:1.25; }
.dg-node-accent { fill:#fcefde; stroke:#b56a05; stroke-width:1; }
.dg-label { fill:#131315; font-size:13px; font-weight:600; }
.dg-sublabel { fill:#56565e; font-size:11px; }
.dg-edge-label { fill:#8a8a93; font-size:10.5px; font-family: ui-monospace, Menlo, monospace; }
.dg-edge { stroke:#8a8a93; stroke-width:1.25; fill:none; }
.dg-edge-primary { stroke:#7531e3; stroke-width:1.5; fill:none; }
.dg-arrow { fill:#8a8a93; }
.dg-arrow-primary { fill:#7531e3; }
""".strip()

FIGURE_RE = re.compile(r"<figure\b[^>]*>(.*?)</figure>", re.DOTALL)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL)
FIGCAP_RE = re.compile(r"<figcaption>(.*?)</figcaption>", re.DOTALL)
ARIA_RE = re.compile(r'aria-label="([^"]*)"')
INLINE_RE = re.compile(
    r"\[([^\]]+)\]\(([^)]+)\)"      # 1,2 link
    r"|\*\*([^*]+)\*\*"             # 3 bold
    r"|(?<!\*)\*([^*]+)\*(?!\*)"    # 4 italic
    r"|`([^`]+)`"                   # 5 code
)


def parse_frontmatter(raw):
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
    data, body = {}, raw
    if m:
        for line in m.group(1).split("\n"):
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
        body = raw[m.end():]
    return data, body


def rewrite_link(url):
    """Riscrive i link relativi del repo in URL assoluti del sito."""
    m = re.match(r"\.\./kb/concetti/([^)#]+)\.md(#.*)?$", url)
    if m:
        return f"{SITE}/kb/{m.group(1)}{m.group(2) or ''}"
    m = re.match(r"\.?/?(\d{2}-)?([^)#/]+)\.md(#.*)?$", url)
    if m and (m.group(1) or "-" in m.group(2)):
        return f"{SITE}/fondamenti/{m.group(2)}{m.group(3) or ''}"
    return url


def inline_runs(text):
    """Testo markdown inline -> lista di run {text, marks[]}."""
    runs, pos = [], 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            runs.append({"text": text[pos:m.start()], "marks": []})
        if m.group(1) is not None:
            runs.append({"text": m.group(1),
                         "marks": [{"type": "link", "href": rewrite_link(m.group(2))}]})
        elif m.group(3) is not None:
            runs.append({"text": m.group(3), "marks": [{"type": "strong"}]})
        elif m.group(4) is not None:
            runs.append({"text": m.group(4), "marks": [{"type": "em"}]})
        elif m.group(5) is not None:
            runs.append({"text": m.group(5), "marks": [{"type": "code"}]})
        pos = m.end()
    if pos < len(text):
        runs.append({"text": text[pos:], "marks": []})
    return [r for r in runs if r["text"]]


def rasterize(svg, out_png):
    styled = SVG_RE.sub(
        lambda mm: mm.group(0).replace(">", f"><style>{DIAGRAM_CSS}</style>", 1), svg, count=1
    )
    subprocess.run(
        ["rsvg-convert", "--background-color=white", "--zoom=2", "-o", out_png],
        input=styled.encode("utf-8"), check=True,
    )


def blocks_from_body(body, figures):
    """Corpo markdown (con sentinelle @@FIGURE:k@@) -> lista di blocchi."""
    blocks, para, items = [], [], None

    def flush_para():
        if para:
            blocks.append({"type": "paragraph", "runs": inline_runs(" ".join(para))})
            para.clear()

    def flush_list():
        nonlocal items
        if items is not None:
            blocks.append({"type": "list", "items": [inline_runs(it) for it in items]})
            items = None

    for line in body.split("\n"):
        s = line.strip()
        if not s:
            flush_para(); flush_list(); continue
        fig = re.match(r"@@FIGURE:(\d+)@@$", s)
        if fig:
            flush_para(); flush_list()
            blocks.append({"type": "image", "figure": figures[int(fig.group(1))]})
            continue
        if s.startswith("## "):
            flush_para(); flush_list()
            blocks.append({"type": "heading", "runs": inline_runs(s[3:].strip())})
            continue
        if s.startswith("# "):
            continue
        if s.startswith("- "):
            flush_para()
            if items is None:
                items = []
            items.append(s[2:].strip())
            continue
        if items is not None:
            items[-1] += " " + s
        else:
            para.append(s)
    flush_para(); flush_list()
    return blocks


def subtitle_from(body):
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p.startswith("#") or p.startswith("<") or p.startswith("@@"):
            continue
        p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p).replace("\n", " ")
        first = re.split(r"(?<=[.?!])\s", p, maxsplit=1)[0]
        return (first[:197] + "...") if len(first) > 200 else first
    return ""


def convert_chapter(path):
    slug_num = os.path.basename(path)[:-3]  # NN-slug
    raw = open(path, encoding="utf-8").read()
    data, body = parse_frontmatter(raw)
    title = data.get("titolo") or slug_num

    out_dir = os.path.join(OUT, slug_num)
    img_dir = os.path.join(out_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    # estrai figure -> sentinelle, rasterizza gli SVG
    figures = []

    def take_figure(m):
        inner = m.group(1)
        svg = SVG_RE.search(inner)
        if not svg:
            return ""  # figura senza svg: rimuovi il blocco
        cap = FIGCAP_RE.search(inner)
        aria = ARIA_RE.search(svg.group(0))
        idx = len(figures)
        png = f"fig{idx + 1}.png"
        rasterize(svg.group(0), os.path.join(img_dir, png))
        figures.append({
            "file": png,
            "caption": (cap.group(1).strip() if cap else ""),
            "alt": (aria.group(1).strip() if aria else (cap.group(1).strip() if cap else title)),
        })
        return f"\n@@FIGURE:{idx}@@\n"

    body = FIGURE_RE.sub(take_figure, body)
    blocks = blocks_from_body(body, figures)
    blocks.append({"type": "paragraph", "runs": [{"text": ATTRIBUTION, "marks": [{"type": "em"}]}]})

    slug = re.sub(r"^\d{2}-", "", slug_num)
    post = {
        "chapter": int(data.get("capitolo") or 0),
        "slug": slug,
        "title": title,
        "subtitle": subtitle_from(body),
        "audience": "only_paid",
        "section": "Fondamenti di AI",
        "concepts": data.get("concetti", ""),
        "canonical_url": f"{SITE}/fondamenti/{slug}",
        "images": figures,
        "blocks": blocks,
    }
    with open(os.path.join(out_dir, "post.json"), "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    write_preview(out_dir, post)
    return post, out_dir


def runs_html(runs):
    out = []
    for r in runs:
        t = (r["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        for mark in r["marks"]:
            if mark["type"] == "link":
                t = f'<a href="{mark["href"]}">{t}</a>'
            elif mark["type"] == "strong":
                t = f"<strong>{t}</strong>"
            elif mark["type"] == "em":
                t = f"<em>{t}</em>"
            elif mark["type"] == "code":
                t = f"<code>{t}</code>"
        out.append(t)
    return "".join(out)


def write_preview(out_dir, post):
    parts = [
        "<meta charset='utf-8'>",
        "<style>body{max-width:680px;margin:2rem auto;font:16px/1.6 -apple-system,sans-serif;"
        "padding:0 1rem}h1{font-size:2rem}h2{margin-top:2rem}img{max-width:100%;border:1px solid #eee;"
        "border-radius:8px}figcaption{color:#888;font-size:.8rem;text-align:center;font-family:monospace}"
        "code{background:#f4f4f4;padding:.1em .3em;border-radius:4px}</style>",
        f"<h1>{post['title']}</h1>",
        f"<p style='color:#666;font-size:1.1rem'>{post['subtitle']}</p>",
        f"<p style='color:#a33;font-size:.8rem'>audience: {post['audience']} &middot; section: {post['section']}</p>",
        "<hr>",
    ]
    for b in post["blocks"]:
        if b["type"] == "heading":
            parts.append(f"<h2>{runs_html(b['runs'])}</h2>")
        elif b["type"] == "paragraph":
            parts.append(f"<p>{runs_html(b['runs'])}</p>")
        elif b["type"] == "list":
            lis = "".join(f"<li>{runs_html(it)}</li>" for it in b["items"])
            parts.append(f"<ul>{lis}</ul>")
        elif b["type"] == "image":
            fig = b["figure"]
            parts.append(
                f"<figure><img src='images/{fig['file']}' alt=\"{fig['alt']}\">"
                f"<figcaption>{fig['caption']}</figcaption></figure>"
            )
    with open(os.path.join(out_dir, "preview.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def main():
    sel = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(
        os.path.join(FONDAMENTI, f)
        for f in os.listdir(FONDAMENTI)
        if re.match(r"^\d{2}-.+\.md$", f) and (sel is None or f.startswith(sel))
    )
    if not files:
        print("Nessun capitolo trovato.")
        return
    for path in files:
        post, out_dir = convert_chapter(path)
        print(f"OK  cap {post['chapter']:>2}  {post['title'][:40]:<40}  "
              f"{len(post['blocks'])} blocchi, {len(post['images'])} immagini  -> {os.path.relpath(out_dir, ROOT)}")


if __name__ == "__main__":
    main()
