import type { Metadata } from "next";
import Link from "next/link";
import { getParti } from "@/lib/fondamenti";
import { Eyebrow } from "@/components/Eyebrow";
import { ArrowRight } from "@/components/Icons";

export const metadata: Metadata = {
  title: "Fondamenti di AI",
  description:
    "La teoria dell'intelligenza artificiale in italiano: percorso in 7 parti e 28 capitoli basato su Russell & Norvig, AIMA 4a edizione.",
};

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
          italiano capitolo per capitolo. {totale} capitoli in 7 parti, basati
          su Russell &amp; Norvig, <em>Intelligenza Artificiale: Un Approccio
          Moderno</em>, 4a edizione italiana (Pearson).
        </p>
      </header>

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
        Pearson Italia (Vol. 1, 2021; Vol. 2, 2022). Ogni capitolo cita volume,
        capitolo e pagine di riferimento.
      </p>
    </div>
  );
}
