import GithubSlugger from "github-slugger";

export interface TocItem {
  depth: 2 | 3;
  text: string;
  id: string;
}

// Rimuove l'H1 iniziale del markdown: il titolo e' gia' reso dall'header di pagina.
export function stripLeadingH1(content: string): string {
  return content.replace(/^\s*#\s+.*\n/, "");
}

// I file KB linkano con path relativi sia altri concetti (es. ./rag.md,
// ../concetti/rag.md) sia i digest (es. ../../digest/2026/05/20.md). Nel web
// vanno riscritti verso /kb/<slug> e /digest/YYYY-MM-DD. I link esterni
// (http/https) restano intatti.
export function rewriteKbLinks(markdown: string): string {
  return (
    markdown
      // Link ai digest: (../)*digest/YYYY/MM/DD.md -> /digest/YYYY-MM-DD
      .replace(
        /\]\((?:\.{1,2}\/)*digest\/(\d{4})\/(\d{2})\/(\d{2})\.md(#[^)]*)?\)/g,
        (_m, y: string, mo: string, d: string) => `](/digest/${y}-${mo}-${d})`,
      )
      // Link ad altri concetti: ./slug.md | ../concetti/slug.md -> /kb/slug
      .replace(
        /\]\((?:\.\/|\.\.\/concetti\/|concetti\/)?([a-z0-9-]+)\.md(#[^)]*)?\)/g,
        (_m, slug: string, hash: string | undefined) => `](/kb/${slug}${hash ?? ""})`,
      )
  );
}

// Estrae l'indice (TOC) dei paragrafi h2/h3. Gli id sono calcolati con lo
// stesso github-slugger usato da rehype-slug, alimentandolo con TUTTE le
// heading in ordine (incluso l'h1) per allineare la numerazione dei duplicati.
export function extractToc(markdown: string): TocItem[] {
  const slugger = new GithubSlugger();
  const toc: TocItem[] = [];
  let inFence = false;

  for (const rawLine of markdown.split("\n")) {
    const line = rawLine.trimEnd();
    if (/^(```|~~~)/.test(line.trim())) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;

    const match = /^(#{1,6})\s+(.*)$/.exec(line);
    if (!match) continue;

    const depth = match[1].length;
    const text = match[2].replace(/\s*#+\s*$/, "").trim();
    const id = slugger.slug(text);

    if (depth === 2 || depth === 3) {
      toc.push({ depth: depth as 2 | 3, text, id });
    }
  }

  return toc;
}
