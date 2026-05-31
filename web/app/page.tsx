import Link from "next/link";
import { getAllDigests } from "@/lib/digest";
import { getAllConcepts } from "@/lib/kb";
import { getModelById } from "@/lib/models";
import { formatLong } from "@/lib/dates";
import { SectionBadge } from "@/components/SectionBadge";
import { ModelCardCompact } from "@/components/ModelCard";
import { Eyebrow } from "@/components/Eyebrow";
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

  return (
    <div className="container-wide flex flex-col gap-20 sm:gap-28">
      {/* Hero */}
      <section className="flex flex-col gap-6 pt-2 sm:pt-8">
        <Eyebrow>Segnali AI · in italiano</Eyebrow>
        <h1 className="max-w-3xl text-balance text-5xl font-semibold leading-[1.02] tracking-tight sm:text-6xl lg:text-7xl">
          AI Deep Dive<span className="text-accent">.</span>
        </h1>
        <p className="max-w-prose text-lg leading-relaxed text-muted sm:text-xl">
          La mia raccolta quotidiana di segnali AI ad alto valore. Curata da una
          routine Claude Code, aggiornata ogni mattina alle 07:00.
        </p>
        <div className="mt-2 flex flex-wrap gap-2.5">
          <Stat value={digests.length} label="digest" href="/digest" />
          <Stat value={concepts.length} label="concetti" href="/kb" />
          <Stat value={4} label="modelli a confronto" href="/radar" />
        </div>
      </section>

      {latest && (
        <section className="flex flex-col gap-6">
          <SectionHeader eyebrow="Ultimo digest" href="/digest" cta="Archivio" />
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
            <span className="text-sm font-medium text-[color:var(--accent-ink)]">
              Leggi tutto →
            </span>
          </Link>
        </section>
      )}

      <section className="flex flex-col gap-6">
        <SectionHeader eyebrow="Dalla knowledge base" href="/kb" cta="Tutti i concetti" />
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
              <span className="mt-auto pt-1 text-sm font-medium text-[color:var(--accent-ink)]">
                Approfondisci →
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-6">
        <SectionHeader eyebrow="Radar rapido" href="/radar" cta="Vai al Radar" />
        <p className="-mt-3 max-w-prose text-[15px] leading-relaxed text-muted">
          Il confronto del momento tra i modelli di frontiera, con focus sui
          financial services.
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
        className="text-sm font-medium text-[color:var(--accent-ink)] underline-offset-4 hover:underline"
      >
        {cta} →
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
    <Link
      href={href}
      className="card card-hover flex items-baseline gap-2 px-4 py-2.5"
    >
      <span className="text-lg font-semibold tabular-nums text-ink">{value}</span>
      <span className="text-sm text-muted">{label}</span>
    </Link>
  );
}
