import Link from "next/link";
import type { KBCardData } from "@/lib/kb";
import { formatShort } from "@/lib/dates";

export function KBCard({ concept }: { concept: KBCardData }) {
  return (
    <Link
      href={`/kb/${concept.slug}`}
      className="group flex h-full flex-col gap-3 rounded-lg border border-line bg-surface p-5 transition-colors hover:border-accent/50"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold leading-tight text-ink">
          {concept.name}
        </h3>
        <span className="chip shrink-0">{concept.categoria}</span>
      </div>
      <p className="line-clamp-3 flex-1 text-sm text-muted">{concept.excerpt}</p>
      <div className="flex items-center gap-3 text-xs text-faint">
        <span>{concept.wordCount.toLocaleString("it-IT")} parole</span>
        {concept.lastUpdated && (
          <span>· aggiornato {formatShort(concept.lastUpdated)}</span>
        )}
      </div>
    </Link>
  );
}
