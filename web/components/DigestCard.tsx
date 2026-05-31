import Link from "next/link";
import type { Digest } from "@/lib/digest";
import { formatLong } from "@/lib/dates";

export function DigestCard({ digest }: { digest: Digest }) {
  return (
    <Link
      href={`/digest/${digest.date}`}
      className="card card-hover group flex flex-col gap-2 p-5"
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
    </Link>
  );
}
