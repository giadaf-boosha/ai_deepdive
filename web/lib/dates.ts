// Formattazione date in italiano. Le date dei contenuti sono stringhe YYYY-MM-DD;
// si ancora il parsing a mezzogiorno UTC per evitare slittamenti di fuso.

function toUtcNoon(isoDate: string): Date {
  return new Date(`${isoDate}T12:00:00Z`);
}

const longFmt = new Intl.DateTimeFormat("it-IT", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "UTC",
});

const shortFmt = new Intl.DateTimeFormat("it-IT", {
  day: "numeric",
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});

const monthFmt = new Intl.DateTimeFormat("it-IT", {
  month: "long",
  year: "numeric",
  timeZone: "UTC",
});

/** "giovedi 29 maggio 2026" */
export function formatLong(isoDate: string): string {
  return longFmt.format(toUtcNoon(isoDate));
}

/** "29 mag 2026" */
export function formatShort(isoDate: string): string {
  return shortFmt.format(toUtcNoon(isoDate));
}

/** chiave mese "2026-05" -> "maggio 2026" */
export function formatMonthKey(monthKey: string): string {
  return monthFmt.format(toUtcNoon(`${monthKey}-01`));
}

/** Normalizza un valore date (string | Date dal frontmatter YAML) in YYYY-MM-DD. */
export function toIsoDate(value: unknown): string | null {
  if (value instanceof Date) {
    return value.toISOString().slice(0, 10);
  }
  if (typeof value === "string") {
    const match = value.match(/\d{4}-\d{2}-\d{2}/);
    if (match) return match[0];
  }
  return null;
}
