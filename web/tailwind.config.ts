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
        accent: {
          DEFAULT: "#c2410c",
          soft: "#ea580c",
          fg: "#ffffff",
        },
        // Tinte per le quattro sezioni tematiche del digest.
        cat: {
          modelli: "#0f766e",
          tool: "#1d4ed8",
          paper: "#b45309",
          business: "#9f1239",
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
