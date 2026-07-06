import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { KB_DIR } from "./content-paths";
import { toIsoDate } from "./dates";

export interface KBConcept {
  slug: string;
  name: string;
  aliases: string[];
  categoria: string;
  created: string | null;
  lastUpdated: string | null;
  content: string; // corpo markdown senza frontmatter
  excerpt: string; // primo paragrafo significativo
  wordCount: number;
}

// Sottoinsieme serializzabile per le card (senza il corpo markdown completo).
export type KBCardData = Pick<
  KBConcept,
  "slug" | "name" | "categoria" | "excerpt" | "wordCount" | "lastUpdated"
>;

export function toCardData(c: KBConcept): KBCardData {
  return {
    slug: c.slug,
    name: c.name,
    categoria: c.categoria,
    excerpt: c.excerpt,
    wordCount: c.wordCount,
    lastUpdated: c.lastUpdated,
  };
}

function listKbFiles(): string[] {
  if (!fs.existsSync(KB_DIR)) return [];
  return fs
    .readdirSync(KB_DIR)
    .filter((f) => f.endsWith(".md"))
    .map((f) => path.join(KB_DIR, f));
}

function toStringArray(value: unknown): string[] {
  if (Array.isArray(value)) return value.map((v) => String(v)).filter(Boolean);
  if (typeof value === "string" && value.trim()) {
    return value
      .replace(/^\[|\]$/g, "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
  }
  return [];
}

// Primo paragrafo di prosa: salta frontmatter (gia' rimosso), heading e righe vuote.
function firstParagraph(content: string): string {
  const lines = content.split("\n");
  let buffer = "";
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      if (buffer) break;
      continue;
    }
    if (line.startsWith("#")) continue;
    buffer += (buffer ? " " : "") + line;
  }
  // Rimuove link markdown mantenendo il testo, e marcatori di enfasi.
  const clean = buffer
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[*_`]/g, "");
  return clean.length > 280 ? `${clean.slice(0, 277).trimEnd()}...` : clean;
}

function parseConceptFile(file: string): KBConcept {
  const raw = fs.readFileSync(file, "utf-8");
  const { data, content } = matter(raw);
  const slug = path.basename(file, ".md");

  const wordCount = content.split(/\s+/).filter(Boolean).length;

  return {
    slug,
    name: typeof data.name === "string" && data.name.trim() ? data.name.trim() : slug,
    aliases: toStringArray(data.aliases),
    categoria:
      typeof data.categoria === "string" && data.categoria.trim()
        ? data.categoria.trim()
        : "altro",
    created: toIsoDate(data.created ?? data.first_seen),
    lastUpdated: toIsoDate(data.last_updated),
    content,
    excerpt: firstParagraph(content),
    wordCount,
  };
}

let cache: KBConcept[] | null = null;

/** Tutti i concetti KB, ordinati alfabeticamente per nome (it-IT). */
export function getAllConcepts(): KBConcept[] {
  if (cache) return cache;
  cache = listKbFiles()
    .map(parseConceptFile)
    .sort((a, b) => a.name.localeCompare(b.name, "it"));
  return cache;
}

export function getConceptSlugs(): string[] {
  return getAllConcepts().map((c) => c.slug);
}

export function getConceptBySlug(slug: string): KBConcept | undefined {
  return getAllConcepts().find((c) => c.slug === slug);
}

export function getCategories(): string[] {
  return Array.from(new Set(getAllConcepts().map((c) => c.categoria))).sort((a, b) =>
    a.localeCompare(b, "it"),
  );
}
