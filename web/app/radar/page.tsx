import type { Metadata } from "next";
import { getModelsData } from "@/lib/models";
import { RadarTabs } from "@/components/RadarTabs";
import { Eyebrow } from "@/components/Eyebrow";

export const metadata: Metadata = {
  title: "Radar modelli AI",
  description:
    "Mappatura comparativa dei principali modelli AI: panoramica, benchmark, casi d'uso, prezzi e privacy.",
};

export default function RadarPage() {
  const data = getModelsData();
  const verifyDate = data.meta.lastUpdated.slice(0, 10);

  return (
    <div className="container-wide flex flex-col gap-8 pt-4">
      <header className="flex flex-col gap-3">
        <Eyebrow>Radar</Eyebrow>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Modelli AI</h1>
        <p className="max-w-prose text-lg text-muted">
          Confronto dei modelli di frontiera con focus sui financial services.
        </p>
        <div className="mt-1 flex items-start gap-3 rounded-xl border border-accent/30 bg-accent/[0.06] px-4 py-3 text-sm text-muted">
          <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-accent" aria-hidden />
          <span>
            Dati aggiornati da routine settimanale —{" "}
            <span className="font-medium text-ink">ultima verifica: {verifyDate}</span>.{" "}
            {data.meta.sourcesChecked.length} fonti ufficiali consultate. Prossimo
            aggiornamento: {data.meta.nextScheduledUpdate.slice(0, 10)}.
          </span>
        </div>
      </header>

      <RadarTabs data={data} />

      <section className="flex flex-col gap-2 border-t border-line pt-6 text-xs text-faint">
        <p className="font-mono uppercase tracking-wider">Fonti verificate</p>
        <ul className="flex flex-col gap-1">
          {data.meta.sourcesChecked.map((s) => (
            <li key={s}>
              <a className="hover:text-accent" href={s} target="_blank" rel="noreferrer">
                {s}
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
