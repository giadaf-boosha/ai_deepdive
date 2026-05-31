import { getLastUpdateLabel } from "@/lib/git";

const REPO_URL = "https://github.com/giadaf-boosha/ai_deepdive";

export function Footer() {
  const lastUpdate = getLastUpdateLabel();

  return (
    <footer className="mt-auto border-t border-line">
      <div className="container-wide flex flex-col gap-6 py-10 sm:flex-row sm:items-end sm:justify-between">
        <div className="flex flex-col gap-2">
          <span className="text-sm font-semibold tracking-tight text-ink">
            AI Deep Dive<span className="text-accent">.</span>
          </span>
          <p className="max-w-sm text-sm text-muted">
            Segnali AI in italiano, generati da una routine Claude Code. Ultimo
            aggiornamento: <span className="text-ink">{lastUpdate}</span>.
          </p>
          <div className="mt-1 flex items-center gap-4 text-sm">
            <a className="link-accent" href={REPO_URL} target="_blank" rel="noreferrer">
              Repository
            </a>
            <span className="text-faint">Italiano · nomi tecnici inalterati</span>
          </div>
        </div>
        <span className="font-mono text-xs uppercase tracking-[0.2em] text-faint">
          ■ Boosha AI
        </span>
      </div>
    </footer>
  );
}
