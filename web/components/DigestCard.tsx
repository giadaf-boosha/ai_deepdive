import Link from "next/link";
import type { Digest } from "@/lib/digest";
import { formatLong } from "@/lib/dates";

export function DigestCard({ digest }: { digest: Digest }) {
  return (
    <Link
      href={`/digest/${digest.date}`}
      className="group flex flex-col gap-2 rounded-lg border border-line bg-surface p-5 transition-colors hover:border-accent/50"
    >
      <div className="flex items-baseline justify-between gap-3">
        <time
          dateTime={digest.date}
          className="text-base font-medium capitalize text-ink"
        >
          {formatLong(digest.date)}
        </time>
        <span className="shrink-0 font-mono text-xs text-faint">{digest.date}</span>
      </div>
      <p className="text-sm text-muted">
        {digest.entriesCount} {digest.entriesCount === 1 ? "voce" : "voci"}
        {digest.sourcesCount != null && ` · ${digest.sourcesCount} fonti`}
      </p>
      {digest.entries.length > 0 && (
        <p className="line-clamp-2 text-sm text-faint">
          {digest.entries.slice(0, 3).map((e) => e.title).join(" · ")}
        </p>
      )}
      <span className="mt-1 text-sm font-medium text-accent opacity-0 transition-opacity group-hover:opacity-100">
        Leggi tutto →
      </span>
    </Link>
  );
}
