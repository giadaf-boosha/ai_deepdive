import { execSync } from "node:child_process";
import { REPO_ROOT } from "./content-paths";
import { getLatestDigest } from "./digest";

// Timestamp dell'ultimo aggiornamento, mostrato nel footer.
// Prova con l'ultimo commit git; in fallback usa la data del digest piu' recente.
export function getLastUpdate(): string {
  try {
    const iso = execSync("git log -1 --format=%cI", {
      cwd: REPO_ROOT,
      encoding: "utf-8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
    if (iso) return iso;
  } catch {
    // git non disponibile a build time: fallback sotto.
  }
  const latest = getLatestDigest();
  return latest?.generatedAt ?? latest?.date ?? "";
}

export function getLastUpdateLabel(): string {
  const raw = getLastUpdate();
  if (!raw) return "n/d";
  const iso = raw.match(/\d{4}-\d{2}-\d{2}/);
  if (!iso) return raw;
  return new Intl.DateTimeFormat("it-IT", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${iso[0]}T12:00:00Z`));
}
