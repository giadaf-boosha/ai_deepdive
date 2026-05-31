import type { Metadata } from "next";
import { getAllDigests } from "@/lib/digest";
import { DigestArchive, type DigestListItem } from "@/components/DigestArchive";
import { Eyebrow } from "@/components/Eyebrow";

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
    <div className="container-wide flex flex-col gap-8 pt-4">
      <header className="flex flex-col gap-3">
        <Eyebrow>Archivio</Eyebrow>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Digest</h1>
        <p className="max-w-prose text-lg text-muted">
          {items.length} digest giornalieri. Ricerca full-text e filtro per mese.
        </p>
      </header>
      <DigestArchive digests={items} />
    </div>
  );
}
