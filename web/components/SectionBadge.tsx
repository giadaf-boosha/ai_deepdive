import type { DigestSection } from "@/lib/digest";

const STYLES: Record<DigestSection, string> = {
  "Modelli & framework": "border-cat-modelli/30 text-cat-modelli",
  "Tool & prodotti": "border-cat-tool/30 text-cat-tool",
  "Paper & ricerca": "border-cat-paper/30 text-cat-paper",
  "Business & strategia": "border-cat-business/30 text-cat-business",
};

const DOT: Record<DigestSection, string> = {
  "Modelli & framework": "bg-cat-modelli",
  "Tool & prodotti": "bg-cat-tool",
  "Paper & ricerca": "bg-cat-paper",
  "Business & strategia": "bg-cat-business",
};

export function SectionBadge({ section }: { section: DigestSection }) {
  return (
    <span className={`chip border ${STYLES[section]}`}>
      <span className={`h-1.5 w-1.5 rounded-full ${DOT[section]}`} aria-hidden />
      {section}
    </span>
  );
}
