"use client";

import { useMemo, useState } from "react";
import type { KBCardData } from "@/lib/kb";
import { KBCard } from "./KBCard";

export function KBIndex({
  concepts,
  categories,
}: {
  concepts: KBCardData[];
  categories: string[];
}) {
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return concepts.filter((c) => {
      if (category !== "all" && c.categoria !== category) return false;
      if (q && !`${c.name} ${c.excerpt}`.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [concepts, category, query]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Cerca un concetto..."
          className="w-full rounded-md border border-line bg-surface px-4 py-2.5 text-sm outline-none transition-colors placeholder:text-faint focus:border-accent"
        />
        <div className="flex flex-wrap gap-1.5">
          <FilterButton active={category === "all"} onClick={() => setCategory("all")}>
            Tutte
          </FilterButton>
          {categories.map((cat) => (
            <FilterButton
              key={cat}
              active={category === cat}
              onClick={() => setCategory(cat)}
            >
              {cat}
            </FilterButton>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((c) => (
          <KBCard key={c.slug} concept={c} />
        ))}
      </div>
      {filtered.length === 0 && (
        <p className="py-8 text-center text-sm text-faint">
          Nessun concetto corrisponde al filtro.
        </p>
      )}
    </div>
  );
}

function FilterButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full border px-3 py-1 text-xs font-medium capitalize transition-colors ${
        active
          ? "border-accent bg-accent text-accent-fg"
          : "border-line text-muted hover:border-accent/50 hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}
