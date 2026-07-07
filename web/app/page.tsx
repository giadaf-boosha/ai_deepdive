import Link from "next/link";
import { getAllDigests } from "@/lib/digest";
import { getAllConcepts } from "@/lib/kb";
import { getModelById, getModels } from "@/lib/models";
import { getAllChapters, PARTI } from "@/lib/fondamenti";
import { getLatestNews } from "@/lib/claudecode";
import { formatLong } from "@/lib/dates";
import { SectionBadge } from "@/components/SectionBadge";
import { ModelCardCompact } from "@/components/ModelCard";
import { MarkdownContent } from "@/components/MarkdownContent";
import { Eyebrow } from "@/components/Eyebrow";
import { ArrowRight, ArrowUpRight } from "@/components/Icons";
import type { ModelId } from "@/lib/models";

export default function HomePage() {
  const digests = getAllDigests();
  const latest = digests[0];
  const concepts = getAllConcepts();
  const recentConcepts = [...concepts]
    .sort((a, b) => (b.lastUpdated ?? "").localeCompare(a.lastUpdated ?? ""))
    .slice(0, 3);
  const quickModels = (["claude", "chatgpt", "gemini"] as ModelId[])
    .map((id) => getModelById(id))
    .filter((m): m is NonNullable<typeof m> => Boolean(m));
  const ccNews = getLatestNews();

  return (
    <div className="container-wide flex flex-col gap-20 sm:gap-28">
      {/* Hero */}
      <section className="flex flex-col gap-6 pt-2 sm:pt-8">
        <Eyebrow>Ogni mattina alle 7</Eyebrow>
        <h1 className="max-w-3xl text-balance text-5xl font-semibold leading-[1.02] tracking-tight sm:text-6xl lg:text-7xl">
          5 AI news<span className="text-accent">.</span>
        </h1>
        <p className="max-w-prose text-lg leading-relaxed text-muted sm:text-xl">
          Ogni giorno escono centinaia di annunci sull&apos;AI. Qui trovi solo
          quelli che contano.
        </p>
        <div className="mt-2 flex flex-wrap gap-2.5">
          <Stat value={digests.length} label="digest" href="/digest" />
          <Stat value={concepts.length} label="concetti spiegati" href="/kb" />
          <Stat value={getAllChapters().length} label="capitoli di fondamenti" href="/fondamenti" />
          <Stat value={getModels().length} label="modelli a confronto" href="/radar" />
        </div>
      </section>

      {latest && (
        <section className="flex flex-col gap-6">
          <SectionHeader eyebrow="L'ultimo digest" href="/digest" cta="Tutti i digest" />
          <Link
            href={`/digest/${latest.date}`}
            className="card card-hover group flex flex-col gap-5 p-6 sm:p-8"
          >
            <div className="flex items-baseline justify-between gap-3">
              <h3 className="text-2xl font-semibold capitalize tracking-tight text-ink sm:text-3xl">
                {formatLong(latest.date)}
              </h3>
              <span className="shrink-0 font-mono text-xs text-faint">{latest.date}</span>
            </div>
            <ul className="flex flex-col gap-3">
              {latest.entries.slice(0, 3).map((e) => (
                <li key={e.title} className="flex flex-col gap-1.5 sm:flex-row sm:items-baseline sm:gap-4">
                  <SectionBadge section={e.section} />
                  <span className="text-[15px] leading-snug text-muted">{e.title}</span>
                </li>
              ))}
              {latest.entries.length === 0 && (
                <li className="text-sm text-faint">
                  Nessuna voce con titolo in evidenza in questo digest.
                </li>
              )}
            </ul>
            <span className="inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)]">
              Leggi tutto <ArrowRight className="h-4 w-4" />
            </span>
          </Link>
        </section>
      )}

      {ccNews && (
        <section className="flex flex-col gap-6">
          <SectionHeader eyebrow="Claude Code · novità" href="/claude-code" cta="Apri la guida" />
          <div className="card flex flex-col gap-4 p-6 sm:p-8">
            <span className="font-mono text-xs text-faint">{formatLong(ccNews.date)}</span>
            {ccNews.hasNews ? (
              <MarkdownContent content={ccNews.body} />
            ) : (
              <p className="text-sm text-muted">
                Nessuna novità rilevante nell&apos;ultimo aggiornamento. La routine
                ricontrolla ogni mattina.
              </p>
            )}
            <Link
              href="/claude-code/whats-new"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)]"
            >
              Tutte le novità <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </section>
      )}

      <section className="flex flex-col gap-6">
        <SectionHeader eyebrow="Dalla knowledge base" href="/kb" cta="Esplora la KB" />
        <p className="-mt-3 max-w-prose text-[15px] leading-relaxed text-muted">
          I concetti tecnici che tornano nei digest, spiegati per bene. Niente
          definizioni da manuale: come funzionano e quando ti servono davvero.
        </p>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {recentConcepts.map((c) => (
            <Link
              key={c.slug}
              href={`/kb/${c.slug}`}
              className="card card-hover group flex flex-col gap-3 p-6"
            >
              <span className="chip self-start">{c.categoria}</span>
              <h3 className="text-lg font-semibold tracking-tight text-ink">{c.name}</h3>
              <p className="line-clamp-4 text-sm leading-relaxed text-muted">{c.excerpt}</p>
              <span className="mt-auto inline-flex items-center gap-1.5 pt-1 text-sm font-medium text-[color:var(--primary-ink)]">
                Approfondisci <ArrowRight className="h-4 w-4" />
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-6">
        <SectionHeader eyebrow="Fondamenti di AI" href="/fondamenti" cta="Inizia il percorso" />
        <p className="-mt-3 max-w-prose text-[15px] leading-relaxed text-muted">
          La teoria dietro le notizie: {getAllChapters().length} capitoli in 7
          parti, dal test di Turing al futuro dell&apos;AI.
        </p>
        <div className="flex flex-wrap gap-2">
          {PARTI.map((p) => (
            <Link
              key={p.numero}
              href={`/fondamenti#parte-${p.numero}`}
              className="chip transition-colors hover:border-primary/50 hover:text-ink"
            >
              <span className="text-faint">{p.numero}.</span> {p.titolo}
            </Link>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-6">
        <SectionHeader eyebrow="Confronto AI" href="/radar" cta="Vai al confronto" />
        <p className="-mt-3 max-w-prose text-[15px] leading-relaxed text-muted">
          Quale strumento per quale lavoro. Modelli, app e tool messi uno di
          fianco all&apos;altro — per scegliere in fretta, senza provare tutto.
        </p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {quickModels.map((m) => (
            <ModelCardCompact key={m.id} model={m} />
          ))}
        </div>
      </section>
    </div>
  );
}

function SectionHeader({
  eyebrow,
  href,
  cta,
}: {
  eyebrow: string;
  href: string;
  cta: string;
}) {
  return (
    <div className="flex items-center justify-between gap-3 border-b border-line pb-3">
      <Eyebrow>{eyebrow}</Eyebrow>
      <Link
        href={href}
        className="inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)] underline-offset-4 hover:underline"
      >
        {cta} <ArrowUpRight className="h-4 w-4" />
      </Link>
    </div>
  );
}

function Stat({
  value,
  label,
  href,
}: {
  value: number;
  label: string;
  href: string;
}) {
  return (
    <Link href={href} className="card card-hover flex items-baseline gap-2 px-4 py-2.5">
      <span className="text-lg font-semibold tabular-nums text-ink">{value}</span>
      <span className="text-sm text-muted">{label}</span>
    </Link>
  );
}
