import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { FONDAMENTI_DIR } from "./content-paths";
import { toIsoDate } from "./dates";

// Le 7 parti di Russell & Norvig, "Intelligenza Artificiale: Un Approccio
// Moderno", 4a ed. italiana (Pearson). I capitoli sono file markdown in
// fondamenti/NN-<slug>.md; lo slug della route e' il filename senza prefisso.
export interface Parte {
  numero: number;
  titolo: string;
  capitoli: [number, number]; // range inclusivo di numeri capitolo
}

export const PARTI: Parte[] = [
  { numero: 1, titolo: "Intelligenza artificiale", capitoli: [1, 2] },
  { numero: 2, titolo: "Risoluzione di problemi", capitoli: [3, 6] },
  { numero: 3, titolo: "Conoscenza, ragionamento e pianificazione", capitoli: [7, 11] },
  { numero: 4, titolo: "Conoscenza incerta e ragionamento in condizioni di incertezza", capitoli: [12, 18] },
  { numero: 5, titolo: "Apprendimento automatico", capitoli: [19, 22] },
  { numero: 6, titolo: "Comunicazione, percezione e azione", capitoli: [23, 26] },
  { numero: 7, titolo: "Conclusioni", capitoli: [27, 28] },
];

export function parteByNumero(numero: number): Parte | undefined {
  return PARTI.find((p) => p.numero === numero);
}

export interface Capitolo {
  slug: string;
  titolo: string;
  capitolo: number;
  parte: number;
  volume: number;
  pagine: string; // range di pagine stampate nel volume di riferimento
  concetti: string[]; // slug KB correlati espliciti
  created: string | null;
  lastUpdated: string | null;
  content: string; // corpo markdown senza frontmatter
  excerpt: string;
  wordCount: number;
}

function listChapterFiles(): string[] {
  if (!fs.existsSync(FONDAMENTI_DIR)) return [];
  return fs
    .readdirSync(FONDAMENTI_DIR)
    .filter((f) => /^\d{2}-.+\.md$/.test(f))
    .map((f) => path.join(FONDAMENTI_DIR, f));
}

function toStringArray(value: unknown): string[] {
  if (Array.isArray(value)) return value.map((v) => String(v)).filter(Boolean);
  return [];
}

// Primo paragrafo di prosa, come in kb.ts.
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
  const clean = buffer
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[*_`]/g, "");
  return clean.length > 280 ? `${clean.slice(0, 277).trimEnd()}...` : clean;
}

function parseChapterFile(file: string): Capitolo {
  const raw = fs.readFileSync(file, "utf-8");
  const { data, content } = matter(raw);
  const slug = path.basename(file, ".md").replace(/^\d{2}-/, "");

  return {
    slug,
    titolo: typeof data.titolo === "string" && data.titolo.trim() ? data.titolo.trim() : slug,
    capitolo: Number(data.capitolo) || 0,
    parte: Number(data.parte) || 0,
    volume: Number(data.volume) || 1,
    pagine: typeof data.pagine === "string" ? data.pagine : String(data.pagine ?? ""),
    concetti: toStringArray(data.concetti),
    created: toIsoDate(data.created),
    lastUpdated: toIsoDate(data.last_updated),
    content,
    excerpt: firstParagraph(content),
    wordCount: content.split(/\s+/).filter(Boolean).length,
  };
}

let cache: Capitolo[] | null = null;

/** Tutti i capitoli, ordinati per numero di capitolo. */
export function getAllChapters(): Capitolo[] {
  if (cache) return cache;
  cache = listChapterFiles()
    .map(parseChapterFile)
    .sort((a, b) => a.capitolo - b.capitolo);
  return cache;
}

export function getChapterSlugs(): string[] {
  return getAllChapters().map((c) => c.slug);
}

export function getChapterBySlug(slug: string): Capitolo | undefined {
  return getAllChapters().find((c) => c.slug === slug);
}

export function getAdjacentChapters(slug: string): {
  prev: Capitolo | undefined;
  next: Capitolo | undefined;
} {
  const all = getAllChapters();
  const i = all.findIndex((c) => c.slug === slug);
  return {
    prev: i > 0 ? all[i - 1] : undefined,
    next: i >= 0 && i < all.length - 1 ? all[i + 1] : undefined,
  };
}

/** Le parti con i rispettivi capitoli presenti, per l'indice. */
export function getParti(): { parte: Parte; capitoli: Capitolo[] }[] {
  const all = getAllChapters();
  return PARTI.map((parte) => ({
    parte,
    capitoli: all.filter((c) => c.parte === parte.numero),
  }));
}
