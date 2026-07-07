import type { Metadata } from "next";
import Link from "next/link";
import { getParti } from "@/lib/fondamenti";
import { Eyebrow } from "@/components/Eyebrow";
import { ArrowRight } from "@/components/Icons";

export const metadata: Metadata = {
  title: "Fondamenti di AI",
  description:
    "La teoria dell'intelligenza artificiale in italiano: percorso in 7 parti e 28 capitoli, dal test di Turing al futuro dell'AI.",
};

// Mappa del percorso: le 7 parti dell'opera come flusso progressivo.
// Layout fisso su viewBox; i nodi linkano le ancore #parte-N dell'indice.
const MAP_NODES: {
  numero: number;
  cap: string;
  righe: [string, string?];
  x: number;
  y: number;
}[] = [
  { numero: 1, cap: "cap 1-2", righe: ["Intelligenza", "artificiale"], x: 8, y: 30 },
  { numero: 2, cap: "cap 3-6", righe: ["Risoluzione", "di problemi"], x: 198, y: 30 },
  { numero: 3, cap: "cap 7-11", righe: ["Conoscenza e", "pianificazione"], x: 388, y: 30 },
  { numero: 4, cap: "cap 12-18", righe: ["Incertezza", "e decisioni"], x: 578, y: 30 },
  { numero: 5, cap: "cap 19-22", righe: ["Apprendimento", "automatico"], x: 107, y: 156 },
  { numero: 6, cap: "cap 23-26", righe: ["Comunicazione,", "percezione, azione"], x: 297, y: 156 },
  { numero: 7, cap: "cap 27-28", righe: ["Conclusioni", "etica e futuro"], x: 487, y: 156 },
];

function MappaPercorso() {
  const W = 166;
  const H = 64;
  return (
    <figure className="diagram">
      <svg
        viewBox="0 0 760 250"
        role="img"
        aria-label="Mappa del percorso: le 7 parti dei Fondamenti di AI in sequenza, dall'intelligenza artificiale alle conclusioni"
      >
        <defs>
          <marker id="arr-map" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="dg-arrow" />
          </marker>
        </defs>
        <line x1="174" y1="62" x2="196" y2="62" className="dg-edge" markerEnd="url(#arr-map)" />
        <line x1="364" y1="62" x2="386" y2="62" className="dg-edge" markerEnd="url(#arr-map)" />
        <line x1="554" y1="62" x2="576" y2="62" className="dg-edge" markerEnd="url(#arr-map)" />
        <path d="M661,94 V125 H190 V153" className="dg-edge" markerEnd="url(#arr-map)" />
        <line x1="273" y1="188" x2="295" y2="188" className="dg-edge" markerEnd="url(#arr-map)" />
        <line x1="463" y1="188" x2="485" y2="188" className="dg-edge" markerEnd="url(#arr-map)" />
        {MAP_NODES.map((n) => (
          <a key={n.numero} href={`#parte-${n.numero}`}>
            <rect x={n.x} y={n.y} width={W} height={H} rx="10" className={n.numero === 1 ? "dg-node-primary" : "dg-node"} />
            <text x={n.x + W / 2} y={n.y + 16} textAnchor="middle" className="dg-edge-label">
              PARTE {n.numero} · {n.cap}
            </text>
            <text x={n.x + W / 2} y={n.y + 34} textAnchor="middle" className="dg-label">
              {n.righe[0]}
            </text>
            {n.righe[1] && (
              <text x={n.x + W / 2} y={n.y + 50} textAnchor="middle" className="dg-sublabel">
                {n.righe[1]}
              </text>
            )}
          </a>
        ))}
      </svg>
      <figcaption>Il percorso in 7 parti — clicca una parte per saltare ai capitoli</figcaption>
    </figure>
  );
}

export default function FondamentiPage() {
  const parti = getParti();
  const totale = parti.reduce((n, p) => n + p.capitoli.length, 0);

  return (
    <div className="container-wide flex flex-col gap-10 pt-4">
      <header className="flex flex-col gap-3">
        <Eyebrow>Teoria, dal principio</Eyebrow>
        <h1 className="max-w-3xl text-balance text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
          Fondamenti di AI<span className="text-accent">.</span>
        </h1>
        <p className="max-w-prose text-lg text-muted">
          I concetti teorici dell&apos;intelligenza artificiale, spiegati in
          italiano capitolo per capitolo. {totale} capitoli in 7 parti, dal
          test di Turing al futuro dell&apos;AI.
        </p>
      </header>

      <MappaPercorso />

      {parti.map(({ parte, capitoli }) => (
        <section
          key={parte.numero}
          id={`parte-${parte.numero}`}
          className="flex flex-col gap-5 scroll-mt-20"
        >
          <div className="flex items-baseline gap-3 border-b border-line pb-3">
            <span className="font-mono text-xs uppercase tracking-wider text-faint">
              Parte {parte.numero}
            </span>
            <h2 className="text-xl font-semibold tracking-tight text-ink sm:text-2xl">
              {parte.titolo}
            </h2>
          </div>
          {capitoli.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {capitoli.map((c) => (
                <Link
                  key={c.slug}
                  href={`/fondamenti/${c.slug}`}
                  className="card card-hover group flex flex-col gap-3 p-6"
                >
                  <span className="font-mono text-xs text-faint">
                    Capitolo {c.capitolo}
                  </span>
                  <h3 className="text-lg font-semibold tracking-tight text-ink">
                    {c.titolo}
                  </h3>
                  <p className="line-clamp-3 text-sm leading-relaxed text-muted">
                    {c.excerpt}
                  </p>
                  <span className="mt-auto inline-flex items-center gap-1.5 pt-1 text-sm font-medium text-[color:var(--primary-ink)]">
                    Leggi il capitolo <ArrowRight className="h-4 w-4" />
                  </span>
                </Link>
              ))}
            </div>
          ) : (
            <p className="text-sm text-faint">Capitoli in preparazione.</p>
          )}
        </section>
      ))}

      <p className="border-t border-line pt-6 text-xs leading-relaxed text-faint">
        I capitoli sono sintesi originali in italiano dei temi trattati
        nell&apos;opera di riferimento: Stuart J. Russell, Peter Norvig,{" "}
        <em>Intelligenza Artificiale: Un Approccio Moderno</em>, 4a edizione,
        Pearson Italia (Vol. 1, 2021; Vol. 2, 2022).
      </p>
    </div>
  );
}
