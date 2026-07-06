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

      {data.changelog.length > 0 && (
        <section className="flex flex-col gap-4 border-t border-line pt-6">
          <p className="font-mono text-xs uppercase tracking-wider text-faint">
            Novita recenti dal radar
          </p>
          <ul className="flex flex-col gap-4">
            {data.changelog.map((entry) => (
              <li key={`${entry.date}-${entry.summary.slice(0, 24)}`} className="flex flex-col gap-1.5">
                <span className="font-mono text-xs text-faint">{entry.date}</span>
                <p className="max-w-prose text-sm leading-relaxed text-muted">{entry.summary}</p>
                <p className="flex flex-wrap gap-x-3 gap-y-1 text-xs">
                  {entry.sources.map((s) => (
                    <a
                      key={s}
                      href={s}
                      target="_blank"
                      rel="noreferrer"
                      className="text-faint underline-offset-2 hover:text-[color:var(--primary-ink)] hover:underline"
                    >
                      {new URL(s).hostname.replace(/^www\./, "")}
                    </a>
                  ))}
                </p>
              </li>
            ))}
          </ul>
        </section>
      )}

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
