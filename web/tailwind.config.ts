import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

// Identita' visiva ai_deepdive: editoriale, tecnica, densa.
// Sfondo quasi-bianco / quasi-nero in base al modo (prefers-color-scheme),
// colore primario forte = burnt orange (non viola AI generico).
const config: Config = {
  darkMode: "media",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "var(--paper)",
        ink: "var(--ink)",
        muted: "var(--muted)",
        faint: "var(--faint)",
        line: "var(--line)",
        surface: "var(--surface)",
        "surface-alt": "var(--surface-alt)",
        // Primario Boosha = viola. Hex statico per supportare i modificatori /opacity.
        primary: {
          DEFAULT: "#7531e3",
          soft: "#9a6bfe",
          ink: "var(--primary-ink)",
          fg: "#fffffa",
        },
        // Secondario Boosha = arancione.
        accent: {
          DEFAULT: "#ed8f12",
          soft: "#f4a53a",
          ink: "var(--accent-ink)",
          fg: "#131315",
        },
        // Tinte per le quattro sezioni tematiche del digest (armonizzate col warm).
        cat: {
          modelli: "#0f766e",
          tool: "#2563eb",
          paper: "#d97706",
          business: "#b91c5c",
        },
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "monospace"],
      },
      maxWidth: {
        prose: "44rem",
        wide: "72rem",
      },
    },
  },
  plugins: [typography],
};

export default config;
