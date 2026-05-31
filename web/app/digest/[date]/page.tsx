import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getDigestByDate,
  getDigestDates,
  getAdjacentDigests,
} from "@/lib/digest";
import { conceptsMentionedIn } from "@/lib/relations";
import { formatLong } from "@/lib/dates";
import { MarkdownContent } from "@/components/MarkdownContent";
import { Eyebrow } from "@/components/Eyebrow";

export const dynamicParams = false;

export function generateStaticParams() {
  return getDigestDates().map((date) => ({ date }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ date: string }>;
}): Promise<Metadata> {
  const { date } = await params;
  const digest = getDigestByDate(date);
  if (!digest) return { title: "Digest non trovato" };
  return {
    title: `Digest ${date}`,
    description: `Segnali AI del ${formatLong(date)}: ${digest.entries
      .slice(0, 3)
      .map((e) => e.title)
      .join("; ")}`,
  };
}

// Rimuove l'H1 iniziale del markdown (lo sostituiamo con l'header di pagina).
function stripLeadingH1(content: string): string {
  return content.replace(/^\s*#\s+.*\n/, "");
}

export default async function DigestPage({
  params,
}: {
  params: Promise<{ date: string }>;
}) {
  const { date } = await params;
  const digest = getDigestByDate(date);
  if (!digest) notFound();

  const { prev, next } = getAdjacentDigests(date);
  const related = conceptsMentionedIn(digest);

  return (
    <div className="container-prose flex flex-col gap-8">
      <div>
        <Link href="/digest" className="link-accent text-sm">
          ← Torna all&apos;archivio
        </Link>
      </div>

      <header className="flex flex-col gap-3 border-b border-line pb-5">
        <Eyebrow>Digest</Eyebrow>
        <h1 className="text-3xl font-semibold capitalize tracking-tight sm:text-4xl">
          {formatLong(digest.date)}
        </h1>
        <p className="flex flex-wrap gap-x-4 gap-y-1 font-mono text-xs text-faint">
          <span>{digest.date}</span>
          <span>
            {digest.entriesCount} {digest.entriesCount === 1 ? "voce" : "voci"}
          </span>
          {digest.sourcesCount != null && <span>{digest.sourcesCount} fonti consultate</span>}
          {digest.sourcesFailed != null && <span>{digest.sourcesFailed} fonti fallite</span>}
        </p>
      </header>

      <article>
        <MarkdownContent content={stripLeadingH1(digest.content)} />
      </article>

      {related.length > 0 && (
        <section className="card flex flex-col gap-4 p-6">
          <Eyebrow>Concetti correlati dalla KB</Eyebrow>
          <div className="flex flex-wrap gap-2">
            {related.map(({ concept, hits }) => (
              <Link
                key={concept.slug}
                href={`/kb/${concept.slug}`}
                className="chip transition-colors hover:border-accent/50 hover:text-ink"
              >
                {concept.name}
                <span className="text-faint">· {hits}</span>
              </Link>
            ))}
          </div>
        </section>
      )}

      <nav className="flex items-stretch justify-between gap-4 border-t border-line pt-6">
        {prev ? (
          <Link
            href={`/digest/${prev.date}`}
            className="group flex flex-col gap-1 text-sm"
          >
            <span className="text-faint">← Precedente</span>
            <span className="font-medium capitalize text-muted group-hover:text-accent">
              {formatLong(prev.date)}
            </span>
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link
            href={`/digest/${next.date}`}
            className="group flex flex-col items-end gap-1 text-right text-sm"
          >
            <span className="text-faint">Successivo →</span>
            <span className="font-medium capitalize text-muted group-hover:text-accent">
              {formatLong(next.date)}
            </span>
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </div>
  );
}
