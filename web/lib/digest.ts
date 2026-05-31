import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { DIGEST_DIR } from "./content-paths";
import { toIsoDate } from "./dates";

// Le quattro sezioni tematiche canoniche del digest, in ordine di rendering.
export const DIGEST_SECTIONS = [
  "Modelli & framework",
  "Tool & prodotti",
  "Paper & ricerca",
  "Business & strategia",
] as const;

export type DigestSection = (typeof DIGEST_SECTIONS)[number];

export interface DigestEntry {
  section: DigestSection;
  title: string;
}

export interface Digest {
  date: string; // YYYY-MM-DD
  year: string;
  month: string; // MM
  monthKey: string; // YYYY-MM
  title: string;
  generatedAt: string | null;
  sourcesCount: number | null;
  sourcesFailed: number | null;
  entriesCount: number;
  entries: DigestEntry[];
  content: string; // corpo markdown senza frontmatter
  searchText: string;
}

function listDigestFiles(): string[] {
  if (!fs.existsSync(DIGEST_DIR)) return [];
  const files: string[] = [];
  // Struttura attesa: digest/YYYY/MM/DD.md
  for (const year of fs.readdirSync(DIGEST_DIR)) {
    const yearDir = path.join(DIGEST_DIR, year);
    if (!fs.statSync(yearDir).isDirectory()) continue;
    for (const month of fs.readdirSync(yearDir)) {
      const monthDir = path.join(yearDir, month);
      if (!fs.statSync(monthDir).isDirectory()) continue;
      for (const file of fs.readdirSync(monthDir)) {
        if (file.endsWith(".md")) files.push(path.join(monthDir, file));
      }
    }
  }
  return files;
}

function asNumber(value: unknown): number | null {
  if (typeof value === "number") return value;
  if (typeof value === "string" && value.trim() !== "" && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return null;
}

function arrayLen(value: unknown): number | null {
  return Array.isArray(value) ? value.length : null;
}

// Estrae le voci (bullet con titolo in grassetto) dalle quattro sezioni
// tematiche, fermandosi a "Note di produzione" / separatore finale.
function parseEntries(content: string): DigestEntry[] {
  const entries: DigestEntry[] = [];
  let current: DigestSection | null = null;

  for (const rawLine of content.split("\n")) {
    const line = rawLine.trim();

    const heading = /^##\s+(.*)$/.exec(line);
    if (heading) {
      const name = heading[1].trim();
      const matched = DIGEST_SECTIONS.find((s) => name.toLowerCase() === s.toLowerCase());
      current = matched ?? null; // "Note di produzione" o altro -> stop di raccolta
      continue;
    }

    if (!current) continue;

    const bullet = /^[-*]\s+\*\*(.+?)\*\*/.exec(line);
    if (bullet) {
      const title = bullet[1].replace(/[:.]\s*$/, "").trim();
      entries.push({ section: current, title });
    }
  }

  return entries;
}

function parseDigestFile(file: string): Digest {
  const raw = fs.readFileSync(file, "utf-8");
  const { data, content } = matter(raw);

  // Data: dal frontmatter (string | Date) o, in fallback, dal path YYYY/MM/DD.
  const rel = path.relative(DIGEST_DIR, file).replace(/\\/g, "/");
  const pathMatch = rel.match(/(\d{4})\/(\d{2})\/(\d{2})\.md$/);
  const fromPath = pathMatch ? `${pathMatch[1]}-${pathMatch[2]}-${pathMatch[3]}` : null;
  const date = toIsoDate(data.date) ?? fromPath ?? rel.replace(/\.md$/, "");

  const [year, month] = date.split("-");
  const entries = parseEntries(content);

  // Conteggio voci: preferisci il frontmatter (EN o IT), altrimenti conta le voci parsate.
  const entriesCount =
    asNumber(data.entries_count) ?? asNumber(data.voci_totali) ?? entries.length;

  const sourcesCount = asNumber(data.sources_count) ?? arrayLen(data.fonti_consultate);
  const sourcesFailed = asNumber(data.sources_failed) ?? arrayLen(data.fonti_fallite);

  return {
    date,
    year,
    month,
    monthKey: `${year}-${month}`,
    title: `AI Deepdive — ${date}`,
    generatedAt: typeof data.generated_at === "string" ? data.generated_at : toIsoDate(data.generated_at),
    sourcesCount,
    sourcesFailed,
    entriesCount,
    entries,
    content,
    searchText: `${date} ${content}`.toLowerCase(),
  };
}

let cache: Digest[] | null = null;

/** Tutti i digest, ordinati per data decrescente (piu' recente prima). */
export function getAllDigests(): Digest[] {
  if (cache) return cache;
  cache = listDigestFiles()
    .map(parseDigestFile)
    .sort((a, b) => b.date.localeCompare(a.date));
  return cache;
}

export function getDigestDates(): string[] {
  return getAllDigests().map((d) => d.date);
}

export function getDigestByDate(date: string): Digest | undefined {
  return getAllDigests().find((d) => d.date === date);
}

/** Digest precedente (piu' vecchio) e successivo (piu' recente) per navigazione. */
export function getAdjacentDigests(date: string): {
  prev: Digest | null;
  next: Digest | null;
} {
  const all = getAllDigests(); // desc
  const idx = all.findIndex((d) => d.date === date);
  if (idx === -1) return { prev: null, next: null };
  return {
    next: idx > 0 ? all[idx - 1] : null, // piu' recente
    prev: idx < all.length - 1 ? all[idx + 1] : null, // piu' vecchio
  };
}

export function getLatestDigest(): Digest | undefined {
  return getAllDigests()[0];
}
