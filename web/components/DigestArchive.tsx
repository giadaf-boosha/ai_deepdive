"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import Fuse from "fuse.js";
import { formatLong, formatMonthKey } from "@/lib/dates";

export interface DigestListItem {
  date: string;
  monthKey: string;
  entriesCount: number;
  sourcesCount: number | null;
  titles: string[];
  text: string;
}

export function DigestArchive({ digests }: { digests: DigestListItem[] }) {
  const [query, setQuery] = useState("");
  const [month, setMonth] = useState("all");

  const months = useMemo(() => {
    const keys = Array.from(new Set(digests.map((d) => d.monthKey)));
    return keys.sort((a, b) => b.localeCompare(a));
  }, [digests]);

  const fuse = useMemo(
    () =>
      new Fuse(digests, {
        keys: ["date", "titles", "text"],
        threshold: 0.35,
        ignoreLocation: true,
        minMatchCharLength: 3,
      }),
    [digests],
  );

  const results = useMemo(() => {
    let list = query.trim() ? fuse.search(query.trim()).map((r) => r.item) : digests;
    if (month !== "all") list = list.filter((d) => d.monthKey === month);
    return list;
  }, [query, month, fuse, digests]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Cerca nei digest (titolo o contenuto)..."
          className="w-full rounded-md border border-line bg-surface px-4 py-2.5 text-sm outline-none transition-colors placeholder:text-faint focus:border-accent"
        />
        <select
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          className="rounded-md border border-line bg-surface px-3 py-2.5 text-sm capitalize outline-none focus:border-accent"
        >
          <option value="all">Tutti i mesi</option>
          {months.map((m) => (
            <option key={m} value={m}>
              {formatMonthKey(m)}
            </option>
          ))}
        </select>
      </div>

      <p className="text-sm text-muted">
        {results.length} {results.length === 1 ? "digest" : "digest"}
        {query.trim() && ` per "${query.trim()}"`}
      </p>

      <ol className="flex flex-col divide-y divide-line overflow-hidden rounded-lg border border-line bg-surface">
        {results.map((d) => (
          <li key={d.date}>
            <Link
              href={`/digest/${d.date}`}
              className="flex flex-col gap-1 px-5 py-4 transition-colors hover:bg-paper sm:flex-row sm:items-center sm:justify-between"
            >
              <span className="flex items-baseline gap-3">
                <time
                  dateTime={d.date}
                  className="font-medium capitalize text-ink"
                >
                  {formatLong(d.date)}
                </time>
                <span className="font-mono text-xs text-faint">{d.date}</span>
              </span>
              <span className="text-sm text-muted">
                {d.entriesCount} {d.entriesCount === 1 ? "voce" : "voci"}
              </span>
            </Link>
          </li>
        ))}
        {results.length === 0 && (
          <li className="px-5 py-8 text-center text-sm text-faint">
            Nessun digest corrisponde alla ricerca.
          </li>
        )}
      </ol>
    </div>
  );
}
