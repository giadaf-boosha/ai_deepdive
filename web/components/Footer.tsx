import { getLastUpdateLabel } from "@/lib/git";
import { ArrowUpRight } from "./Icons";

const REPO_URL = "https://github.com/giadaf-boosha/ai_deepdive";
const BOOSHA_URL = "https://boosha.it/";

export function Footer() {
  const lastUpdate = getLastUpdateLabel();

  return (
    <footer className="mt-auto border-t border-line">
      <div className="container-wide flex flex-col gap-6 py-10 sm:flex-row sm:items-end sm:justify-between">
        <div className="flex flex-col gap-2">
          <span className="text-sm font-semibold tracking-tight text-ink">
            AI Deep Dive<span className="text-accent">.</span>
          </span>
          <p className="max-w-md text-sm leading-relaxed text-muted">
            Ultimo aggiornamento: <span className="text-ink">{lastUpdate}</span>.
          </p>
          <div className="mt-1 flex items-center gap-4 text-sm">
            <a
              className="link-primary inline-flex items-center gap-1"
              href={REPO_URL}
              target="_blank"
              rel="noreferrer"
            >
              Repository <ArrowUpRight className="h-3.5 w-3.5" />
            </a>
          </div>
        </div>
        <a
          href={BOOSHA_URL}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1.5 font-mono text-xs uppercase tracking-[0.2em] text-faint transition-colors hover:text-[color:var(--primary-ink)]"
        >
          ■ Boosha AI <ArrowUpRight className="h-3 w-3" />
        </a>
      </div>
    </footer>
  );
}
