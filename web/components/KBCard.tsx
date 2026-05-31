import Link from "next/link";
import type { KBCardData } from "@/lib/kb";
import { formatShort } from "@/lib/dates";

export function KBCard({ concept }: { concept: KBCardData }) {
  return (
    <Link
      href={`/kb/${concept.slug}`}
      className="card card-hover group flex h-full flex-col gap-3 p-5"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold leading-tight tracking-tight text-ink">
          {concept.name}
        </h3>
        <span className="chip shrink-0">{concept.categoria}</span>
      </div>
      <p className="line-clamp-3 flex-1 text-sm leading-relaxed text-muted">
        {concept.excerpt}
      </p>
      <div className="flex items-center gap-2 text-xs text-faint">
        <span>{concept.wordCount.toLocaleString("it-IT")} parole</span>
        {concept.lastUpdated && (
          <span>· aggiornato {formatShort(concept.lastUpdated)}</span>
        )}
      </div>
    </Link>
  );
}
