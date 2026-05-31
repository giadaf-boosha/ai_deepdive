import type { Digest } from "./digest";
import type { KBConcept } from "./kb";
import { getAllConcepts } from "./kb";
import { getAllDigests } from "./digest";

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
