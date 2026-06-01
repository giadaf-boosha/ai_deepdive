import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const CC_DIR = path.join(process.cwd(), "content", "claude-code");
const DOCS_DIR = path.join(CC_DIR, "docs");
const ARCHIVE = path.join(CC_DIR, "whats-new-archive.md");

export const CC_REPO_URL = "https://github.com/giadaf-boosha/claude-code";

export interface CCDoc {
  slug: string;
  title: string;
  order: string;
  source: string;
  content: string;
  excerpt: string;
  wordCount: number;
}

export interface WhatsNewDay {
  date: string; // YYYY-MM-DD
  body: string; // markdown della sezione
  hasNews: boolean;
  entryCount: number;
}

function firstParagraph(content: string): string {
  for (const rawLine of content.split("\n")) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#") || line.startsWith(">") || line.startsWith("|")) continue;
    const clean = line
      .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
      .replace(/[*_`]/g, "");
    if (clean.length < 8) continue;
    return clean.length > 220 ? `${clean.slice(0, 217).trimEnd()}...` : clean;
  }
  return "";
}

let docsCache: CCDoc[] | null = null;

export function getAllDocs(): CCDoc[] {
  if (docsCache) return docsCache;
  if (!fs.existsSync(DOCS_DIR)) return [];
  docsCache = fs
    .readdirSync(DOCS_DIR)
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const raw = fs.readFileSync(path.join(DOCS_DIR, f), "utf-8");
      const { data, content } = matter(raw);
      return {
        slug: typeof data.slug === "string" ? data.slug : f.replace(/\.md$/, ""),
        title: typeof data.title === "string" ? data.title : f.replace(/\.md$/, ""),
        order: data.order != null ? String(data.order).padStart(3, "0") : "999",
        source: typeof data.source === "string" ? data.source : CC_REPO_URL,
        content,
        excerpt: firstParagraph(content),
        wordCount: content.split(/\s+/).filter(Boolean).length,
      };
    })
    .sort((a, b) => a.order.localeCompare(b.order));
  return docsCache;
}

export function getDocSlugs(): string[] {
  return getAllDocs().map((d) => d.slug);
}

export function getDocBySlug(slug: string): CCDoc | undefined {
  return getAllDocs().find((d) => d.slug === slug);
}

// Parsa whats-new-archive.md nelle sezioni ## YYYY-MM-DD.
export function getWhatsNew(): WhatsNewDay[] {
  if (!fs.existsSync(ARCHIVE)) return [];
  const raw = fs.readFileSync(ARCHIVE, "utf-8");
  const days: WhatsNewDay[] = [];
  const parts = raw.split(/^##\s+(\d{4}-\d{2}-\d{2})\s*$/m);
  // parts: [preamble, date1, body1, date2, body2, ...]
  for (let i = 1; i < parts.length; i += 2) {
    const date = parts[i];
    const body = (parts[i + 1] ?? "").replace(/^\s*-{3,}\s*$/gm, "").trim();
    const bullets = (body.match(/^[-*]\s+/gm) || []).length;
    const hasNews = !/nessuna novita/i.test(body) && bullets > 0;
    days.push({ date, body, hasNews, entryCount: bullets });
  }
  return days.sort((a, b) => b.date.localeCompare(a.date));
}

export function getLatestNews(): WhatsNewDay | undefined {
  return getWhatsNew().find((d) => d.hasNews) ?? getWhatsNew()[0];
}
