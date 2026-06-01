import Link from "next/link";
import { getAllDigests } from "@/lib/digest";
import { getAllConcepts } from "@/lib/kb";
import { getModelById } from "@/lib/models";
import { getAllDocs } from "@/lib/claudecode";
import { formatLong } from "@/lib/dates";
import { SectionBadge } from "@/components/SectionBadge";
import { ModelCardCompact } from "@/components/ModelCard";
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
  const ccDocs = getAllDocs();

  return (
    <div className="container-wide flex flex-col gap-20 sm:gap-28">
      {/* Hero */}
      <section className="flex flex-col gap-6 pt-2 sm:pt-8">
        <Eyebrow>Segnali AI · ogni mattina</Eyebrow>
        <h1 className="max-w-3xl text-balance text-5xl font-semibold leading-[1.02] tracking-tight sm:text-6xl lg:text-7xl">
          L&apos;AI che conta<span className="text-accent">.</span> Senza il rumore.
        </h1>
        <p className="max-w-prose text-lg leading-relaxed text-muted sm:text-xl">
          Ogni giorno escono centinaia di annunci sull&apos;AI. Qui trovi solo
          quelli che spostano davvero qualcosa — pochi, scelti a mano, in
          italiano. Li raccoglie una routine Claude Code, ogni mattina alle 07:00.
        </p>
        <div className="mt-2 flex flex-wrap gap-2.5">
          <Stat value={digests.length} label="digest" href="/digest" />
          <Stat value={concepts.length} label="concetti spiegati" href="/kb" />
          <Stat value={4} label="modelli a confronto" href="/radar" />
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
        <SectionHeader eyebrow="Modelli e tools AI" href="/radar" cta="Vai al confronto" />
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

      {ccDocs.length > 0 && (
        <section className="flex flex-col gap-6">
          <SectionHeader eyebrow="Guida Claude Code" href="/claude-code" cta="Apri la guida" />
          <Link
            href="/claude-code"
            className="card card-hover group flex flex-col gap-4 p-6 sm:p-8"
          >
            <h3 className="max-w-2xl text-xl font-semibold tracking-tight text-ink sm:text-2xl">
              Padroneggiare Claude Code, in italiano.
            </h3>
            <p className="max-w-prose text-[15px] leading-relaxed text-muted">
              {ccDocs.length} capitoli su CLI, routines, hooks, MCP, subagents e
              workflow agentici — più il <span className="text-ink">What&apos;s new</span> aggiornato
              ogni giorno.
            </p>
            <span className="inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)]">
              Apri la guida <ArrowRight className="h-4 w-4" />
            </span>
          </Link>
        </section>
      )}
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
