import type { Digest } from "./digest";
import type { KBConcept } from "./kb";
import type { Capitolo } from "./fondamenti";
import { getAllConcepts } from "./kb";
import { getAllDigests } from "./digest";
import { getAllChapters } from "./fondamenti";

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Termini di un concetto = nome + alias, ordinati per lunghezza decrescente
// cosi' i match piu' specifici prevalgono. Match come parola intera, case-insensitive.
function conceptMatcher(concept: KBConcept): RegExp {
  const terms = [concept.name, ...concept.aliases]
    .map((t) => t.trim())
    .filter((t) => t.length >= 2)
    .sort((a, b) => b.length - a.length)
    .map(escapeRegExp);
  return new RegExp(`(?<![\\w-])(?:${terms.join("|")})(?![\\w-])`, "gi");
}

function countOccurrences(text: string, re: RegExp): number {
  const matches = text.match(re);
  return matches ? matches.length : 0;
}

/** Concetti KB menzionati in un digest, ordinati per numero di occorrenze. */
export function conceptsMentionedIn(
  digest: Digest,
  limit = 6,
): { concept: KBConcept; hits: number }[] {
  const text = digest.content;
  return getAllConcepts()
    .map((concept) => ({ concept, hits: countOccurrences(text, conceptMatcher(concept)) }))
    .filter((r) => r.hits > 0)
    .sort((a, b) => b.hits - a.hits)
    .slice(0, limit);
}

/** Digest che citano un concetto, ordinati per data decrescente. */
export function digestsMentioning(concept: KBConcept, limit = 12): Digest[] {
  const re = conceptMatcher(concept);
  return getAllDigests()
    .filter((d) => countOccurrences(d.content, re) > 0)
    .slice(0, limit);
}

/** Numero totale di digest che citano un concetto. */
export function digestMentionCount(concept: KBConcept): number {
  const re = conceptMatcher(concept);
  return getAllDigests().filter((d) => countOccurrences(d.content, re) > 0).length;
}

/** Concetti correlati: condividono almeno una categoria, esclusi se stessi. */
export function relatedConcepts(concept: KBConcept, limit = 5): KBConcept[] {
  return getAllConcepts()
    .filter((c) => c.slug !== concept.slug && c.categoria === concept.categoria)
    .slice(0, limit);
}

// Soglia sui match regex nei capitoli: i testi sono lunghi e gli alias corti
// (es. "agent") matchano ovunque; sotto 2 occorrenze il legame non e' segnale.
const CHAPTER_MATCH_THRESHOLD = 2;

/** Concetti KB correlati a un capitolo: prima gli slug espliciti del frontmatter, poi i match testuali. */
export function kbConceptsInChapter(cap: Capitolo, limit = 6): KBConcept[] {
  const all = getAllConcepts();
  const explicit = cap.concetti
    .map((slug) => all.find((c) => c.slug === slug))
    .filter((c): c is KBConcept => Boolean(c));
  const explicitSlugs = new Set(explicit.map((c) => c.slug));
  const matched = all
    .filter((c) => !explicitSlugs.has(c.slug))
    .map((concept) => ({
      concept,
      hits: countOccurrences(cap.content, conceptMatcher(concept)),
    }))
    .filter((r) => r.hits >= CHAPTER_MATCH_THRESHOLD)
    .sort((a, b) => b.hits - a.hits)
    .map((r) => r.concept);
  return [...explicit, ...matched].slice(0, limit);
}

/** Capitoli fondamenti che trattano un concetto KB, in ordine di capitolo. */
export function chaptersMentioning(concept: KBConcept, limit = 6): Capitolo[] {
  const re = conceptMatcher(concept);
  return getAllChapters()
    .filter(
      (cap) =>
        cap.concetti.includes(concept.slug) ||
        countOccurrences(cap.content, re) >= CHAPTER_MATCH_THRESHOLD,
    )
    .slice(0, limit);
}
