import { getLastUpdateLabel } from "@/lib/git";

const REPO_URL = "https://github.com/giadaf-boosha/ai_deepdive";

export function Footer() {
  const lastUpdate = getLastUpdateLabel();

  return (
    <footer className="border-t border-line">
      <div className="container-wide flex flex-col gap-2 py-8 text-sm text-muted sm:flex-row sm:items-center sm:justify-between">
        <p>
          Generato da routine Claude Code — ultimo aggiornamento:{" "}
          <span className="font-medium text-ink">{lastUpdate}</span>
        </p>
        <p className="flex items-center gap-4">
          <a className="link-accent" href={REPO_URL} target="_blank" rel="noreferrer">
            Repository
          </a>
          <span className="text-faint">Italiano sempre · nomi tecnici inalterati</span>
        </p>
      </div>
    </footer>
  );
}
