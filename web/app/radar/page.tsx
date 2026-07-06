import type { Metadata } from "next";
import { getModelsData } from "@/lib/models";
import { RadarTabs } from "@/components/RadarTabs";
import { Eyebrow } from "@/components/Eyebrow";

export const metadata: Metadata = {
  title: "Confronto AI",
  description:
    "Modelli, app e tool AI messi uno di fianco all'altro: cosa usare per cosa, feature, benchmark e prezzi. In italiano.",
};

export default function RadarPage() {
  const data = getModelsData();
  const verifyDate = data.meta.lastUpdated.slice(0, 10);

  return (
    <div className="container-wide flex flex-col gap-8 pt-4">
      <header className="flex flex-col gap-3">
        <Eyebrow>Radar settimanale</Eyebrow>
        <h1 className="max-w-3xl text-balance text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
          Confronto AI<span className="text-accent">.</span>
        </h1>
        <p className="max-w-prose text-lg text-muted">
          Quale strumento per quale lavoro. Distinguiamo il <span className="text-ink">modello</span> (il
          motore) dall&apos;<span className="text-ink">app</span> (il prodotto), e mappiamo i tool per
          ogni esigenza creativa.
        </p>
        <div className="mt-1 flex items-start gap-3 rounded-xl border border-primary/30 bg-primary/[0.06] px-4 py-3 text-sm text-muted">
          <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-primary" aria-hidden />
          <span>
            Aggiornato da routine settimanale —{" "}
            <span className="font-medium text-ink">ultima verifica: {verifyDate}</span>.{" "}
            {data.meta.sourcesChecked.length} fonti ufficiali consultate. Prossimo aggiornamento:{" "}
            {data.meta.nextScheduledUpdate.slice(0, 10)}.
          </span>
        </div>
      </header>

      <RadarTabs data={data} />

      <section className="flex flex-col gap-2 border-t border-line pt-6 text-xs text-faint">
        <p className="font-mono uppercase tracking-wider">Fonti verificate</p>
        <ul className="flex flex-col gap-1">
          {data.meta.sourcesChecked.map((s) => (
            <li key={s}>
              <a className="hover:text-[color:var(--primary-ink)]" href={s} target="_blank" rel="noreferrer">
                {s}
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
