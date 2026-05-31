import type { TocItem } from "@/lib/markdown";

export function Toc({ items }: { items: TocItem[] }) {
  if (items.length === 0) return null;
  return (
    <nav aria-label="Indice" className="text-sm">
      <p className="mb-3 font-mono text-xs uppercase tracking-wider text-faint">
        In questa pagina
      </p>
      <ul className="flex flex-col gap-1.5 border-l border-line">
        {items.map((item) => (
          <li key={item.id} className={item.depth === 3 ? "pl-6" : "pl-3"}>
            <a
              href={`#${item.id}`}
              className="block text-muted transition-colors hover:text-accent"
            >
              {item.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
