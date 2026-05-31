import type { Metadata } from "next";
import { getAllDigests } from "@/lib/digest";
import { DigestArchive, type DigestListItem } from "@/components/DigestArchive";

export const metadata: Metadata = {
  title: "Archivio digest",
  description: "Tutti i digest giornalieri AI Deep Dive, in ordine cronologico.",
};

export default function DigestArchivePage() {
  const items: DigestListItem[] = getAllDigests().map((d) => ({
    date: d.date,
    monthKey: d.monthKey,
    entriesCount: d.entriesCount,
    sourcesCount: d.sourcesCount,
    titles: d.entries.map((e) => e.title),
    text: d.searchText,
  }));

  return (
    <div className="container-wide flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold tracking-tight">Archivio digest</h1>
        <p className="text-muted">
          {items.length} digest giornalieri. Ricerca full-text e filtro per mese.
        </p>
      </header>
      <DigestArchive digests={items} />
    </div>
  );
}
