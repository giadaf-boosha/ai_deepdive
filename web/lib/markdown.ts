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

// Link ai digest: (../)*digest/YYYY/MM/DD.md -> /digest/YYYY-MM-DD
function rewriteDigestLinks(markdown: string): string {
  return markdown.replace(
    /\]\((?:\.{1,2}\/)*digest\/(\d{4})\/(\d{2})\/(\d{2})\.md(#[^)]*)?\)/g,
    (_m, y: string, mo: string, d: string) => `](/digest/${y}-${mo}-${d})`,
  );
}

// Link ai capitoli fondamenti: (../)*fondamenti/NN-slug.md -> /fondamenti/slug
function rewriteFondamentiRefs(markdown: string): string {
  return markdown.replace(
    /\]\((?:\.{1,2}\/)*fondamenti\/(?:\d{2}-)?([a-z0-9-]+)\.md(#[^)]*)?\)/g,
    (_m, slug: string, hash: string | undefined) => `](/fondamenti/${slug}${hash ?? ""})`,
  );
}

// I file KB linkano con path relativi altri concetti (es. ./rag.md,
// ../concetti/rag.md), i digest (es. ../../digest/2026/05/20.md) e i capitoli
// fondamenti (es. ../fondamenti/01-introduzione.md). Nel web vanno riscritti
// verso /kb/<slug>, /digest/YYYY-MM-DD e /fondamenti/<slug>. I link esterni
// (http/https) restano intatti.
export function rewriteKbLinks(markdown: string): string {
  return (
    rewriteFondamentiRefs(rewriteDigestLinks(markdown))
      // Link ad altri concetti: ./slug.md | ../concetti/slug.md -> /kb/slug
      .replace(
        /\]\((?:\.\/|\.\.\/concetti\/|concetti\/)?([a-z0-9-]+)\.md(#[^)]*)?\)/g,
        (_m, slug: string, hash: string | undefined) => `](/kb/${slug}${hash ?? ""})`,
      )
  );
}

// I capitoli fondamenti linkano i concetti KB (es. ../kb/concetti/rag.md),
// altri capitoli (es. ./02-agenti-intelligenti.md) e i digest.
export function rewriteFondamentiLinks(markdown: string): string {
  return (
    rewriteDigestLinks(markdown)
      // Concetti KB: (../)*kb/concetti/slug.md -> /kb/slug
      .replace(
        /\]\((?:\.{1,2}\/)*kb\/concetti\/([a-z0-9-]+)\.md(#[^)]*)?\)/g,
        (_m, slug: string, hash: string | undefined) => `](/kb/${slug}${hash ?? ""})`,
      )
      // Capitoli fratelli: ./NN-slug.md | NN-slug.md | slug.md -> /fondamenti/slug
      .replace(
        /\]\((?:\.\/)?(?:\d{2}-)?([a-z0-9-]+)\.md(#[^)]*)?\)/g,
        (_m, slug: string, hash: string | undefined) => `](/fondamenti/${slug}${hash ?? ""})`,
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
