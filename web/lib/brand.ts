import type { ModelId } from "./models";

// Colori brand dei provider per card e barre benchmark. Modulo separato da
// models.ts per non trascinare models.json nel bundle client.
const BRAND: Record<string, string> = {
  claude: "#e8901b",
  chatgpt: "#0f766e",
  gemini: "#2563eb",
};

const FALLBACK = "#7531e3";

export function brandColor(id: ModelId): string {
  return BRAND[id] ?? FALLBACK;
}
