import type { Metadata } from "next";
import Link from "next/link";
import { getAllDocs, getWhatsNew, CC_REPO_URL } from "@/lib/claudecode";
import { formatLong } from "@/lib/dates";
import { Eyebrow } from "@/components/Eyebrow";
import { MarkdownContent } from "@/components/MarkdownContent";
import { ArrowRight, ArrowUpRight } from "@/components/Icons";

export const metadata: Metadata = {
  title: "Claude Code",
  description:
    "La guida a Claude Code in italiano: capitoli operativi, concetti e novità giornaliere. Manutenuta da Boosha.",
};

export default function ClaudeCodePage() {
  const docs = getAllDocs();
  const news = getWhatsNew();
  const latestNews = news.find((d) => d.hasNews) ?? news[0];

  return (
    <div className="container-wide flex flex-col gap-14 pt-4">
      <header className="flex flex-col gap-4">
        <Eyebrow>Guida · Claude Code</Eyebrow>
        <h1 className="max-w-3xl text-balance text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
          Claude Code, spiegato per bene<span className="text-accent">.</span>
        </h1>
        <p className="max-w-prose text-lg leading-relaxed text-muted">
          La guida completa in italiano: CLI, IDE, routines, hooks, MCP,
          subagents e workflow agentici. {docs.length} capitoli, aggiornati ogni
          giorno dalla routine dedicata.
        </p>
        <a
          href={CC_REPO_URL}
          target="_blank"
          rel="noreferrer"
          className="btn-outline self-start"
        >
          Repo su GitHub <ArrowUpRight className="h-4 w-4" />
        </a>
      </header>

      {latestNews && (
        <section className="flex flex-col gap-5">
          <div className="flex items-center justify-between gap-3 border-b border-line pb-3">
            <Eyebrow>What&apos;s new</Eyebrow>
            {news.length > 0 && (
              <Link
                href="/claude-code/whats-new"
                className="inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)] hover:underline"
              >
                Archivio aggiornamenti <ArrowUpRight className="h-4 w-4" />
              </Link>
            )}
          </div>
          <div className="card flex flex-col gap-3 p-6">
            <span className="font-mono text-xs text-faint">
              {formatLong(latestNews.date)}
            </span>
            {latestNews.hasNews ? (
              <MarkdownContent content={latestNews.body} />
            ) : (
              <p className="text-sm text-muted">
                Nessuna novità rilevante nell&apos;ultimo aggiornamento. La
                routine ricontrolla ogni mattina alle 07:00.
              </p>
            )}
          </div>
        </section>
      )}

      <section className="flex flex-col gap-5">
        <div className="border-b border-line pb-3">
          <Eyebrow>I capitoli</Eyebrow>
        </div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {docs.map((doc) => (
            <Link
              key={doc.slug}
              href={`/claude-code/${doc.slug}`}
              className="card card-hover group flex flex-col gap-2 p-5"
            >
              <h2 className="text-base font-semibold tracking-tight text-ink">
                {doc.title}
              </h2>
              {doc.excerpt && (
                <p className="line-clamp-2 text-sm leading-relaxed text-muted">
                  {doc.excerpt}
                </p>
              )}
              <span className="mt-1 inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)]">
                Leggi <ArrowRight className="h-4 w-4" />
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
