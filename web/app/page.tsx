import Link from "next/link";
import { getAllDigests } from "@/lib/digest";
import { getAllConcepts } from "@/lib/kb";
import { getModelById } from "@/lib/models";
import { formatLong } from "@/lib/dates";
import { SectionBadge } from "@/components/SectionBadge";
import { ModelCardCompact } from "@/components/ModelCard";
import type { ModelId } from "@/lib/models";

export default function HomePage() {
  const digests = getAllDigests();
  const latest = digests[0];
  const recentConcepts = [...getAllConcepts()]
    .sort((a, b) => (b.lastUpdated ?? "").localeCompare(a.lastUpdated ?? ""))
    .slice(0, 3);
  const quickModels = (["claude", "chatgpt", "gemini"] as ModelId[])
    .map((id) => getModelById(id))
    .filter((m): m is NonNullable<typeof m> => Boolean(m));

  return (
    <div className="container-wide flex flex-col gap-16">
      <section className="flex flex-col gap-3 pt-6">
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
          AI Deep Dive
        </h1>
        <p className="max-w-prose text-lg text-muted">
          La mia raccolta quotidiana di segnali AI, in italiano. Curata da una
          routine Claude Code, aggiornata ogni mattina alle 07:00.
        </p>
      </section>

      {latest && (
        <section className="flex flex-col gap-5">
          <SectionHeader title="Ultimo digest" href="/digest" cta="Archivio →" />
          <Link
            href={`/digest/${latest.date}`}
            className="group flex flex-col gap-4 rounded-xl border border-line bg-surface p-6 transition-colors hover:border-accent/50"
          >
            <div className="flex items-baseline justify-between gap-3">
              <h3 className="text-xl font-semibold capitalize text-ink">
                {formatLong(latest.date)}
              </h3>
              <span className="font-mono text-xs text-faint">{latest.date}</span>
            </div>
            <ul className="flex flex-col gap-2.5">
              {latest.entries.slice(0, 3).map((e) => (
                <li key={e.title} className="flex flex-col gap-1 sm:flex-row sm:items-center sm:gap-3">
                  <SectionBadge section={e.section} />
                  <span className="text-sm text-muted">{e.title}</span>
                </li>
              ))}
              {latest.entries.length === 0 && (
                <li className="text-sm text-faint">
                  Nessuna voce con titolo in evidenza in questo digest.
                </li>
              )}
            </ul>
            <span className="text-sm font-medium text-accent">Leggi tutto →</span>
          </Link>
        </section>
      )}

      <section className="flex flex-col gap-5">
        <SectionHeader title="Dalla knowledge base" href="/kb" cta="Tutti i concetti →" />
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          {recentConcepts.map((c) => (
            <Link
              key={c.slug}
              href={`/kb/${c.slug}`}
              className="group flex flex-col gap-2 rounded-lg border border-line bg-surface p-5 transition-colors hover:border-accent/50"
            >
              <h3 className="font-semibold text-ink">{c.name}</h3>
              <p className="line-clamp-4 text-sm text-muted">{c.excerpt}</p>
              <span className="mt-1 text-sm font-medium text-accent">Approfondisci →</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="flex flex-col gap-5">
        <SectionHeader title="Radar rapido" href="/radar" cta="Vai al Radar →" />
        <p className="-mt-2 max-w-prose text-sm text-muted">
          Il confronto del momento tra i modelli di frontiera.
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
  title,
  href,
  cta,
}: {
  title: string;
  href: string;
  cta: string;
}) {
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-line pb-2">
      <h2 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">
        {title}
      </h2>
      <Link href={href} className="link-accent text-sm">
        {cta}
      </Link>
    </div>
  );
}
