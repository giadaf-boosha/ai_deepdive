import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getConceptBySlug, getConceptSlugs } from "@/lib/kb";
import {
  digestsMentioning,
  digestMentionCount,
  relatedConcepts,
  chaptersMentioning,
} from "@/lib/relations";
import { extractToc, stripLeadingH1 } from "@/lib/markdown";
import { formatLong, formatShort } from "@/lib/dates";
import { MarkdownContent } from "@/components/MarkdownContent";
import { Toc } from "@/components/Toc";
import { Eyebrow } from "@/components/Eyebrow";

export const dynamicParams = false;

export function generateStaticParams() {
  return getConceptSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const concept = getConceptBySlug(slug);
  if (!concept) return { title: "Concetto non trovato" };
  return { title: concept.name, description: concept.excerpt };
}

export default async function KBConceptPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const concept = getConceptBySlug(slug);
  if (!concept) notFound();

  const body = stripLeadingH1(concept.content);
  const toc = extractToc(body);
  const mentions = digestsMentioning(concept);
  const mentionCount = digestMentionCount(concept);
  const related = relatedConcepts(concept);
  const capitoli = chaptersMentioning(concept);

  return (
    <div className="container-wide grid grid-cols-1 gap-10 lg:grid-cols-[1fr_16rem]">
      <div className="flex min-w-0 flex-col gap-8">
        <div>
          <Link href="/kb" className="link-primary text-sm">
            ← Knowledge base
          </Link>
        </div>

        <header className="flex flex-col gap-3 border-b border-line pb-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="chip capitalize">{concept.categoria}</span>
            {concept.aliases.slice(0, 4).map((a) => (
              <span key={a} className="font-mono text-xs text-faint">
                {a}
              </span>
            ))}
          </div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{concept.name}</h1>
          <p className="flex flex-wrap gap-x-4 font-mono text-xs text-faint">
            <span>{concept.wordCount.toLocaleString("it-IT")} parole</span>
            {concept.lastUpdated && (
              <span>ultima modifica: {formatShort(concept.lastUpdated)}</span>
            )}
            <span>
              menzionato in {mentionCount} {mentionCount === 1 ? "digest" : "digest"}
            </span>
          </p>
        </header>

        <article>
          <MarkdownContent content={body} rewriteKb />
        </article>

        {mentions.length > 0 && (
          <section className="card flex flex-col gap-4 p-6">
            <Eyebrow>Citato nei digest</Eyebrow>
            <ul className="flex flex-col gap-1.5">
              {mentions.map((d) => (
                <li key={d.date}>
                  <Link
                    href={`/digest/${d.date}`}
                    className="text-sm capitalize text-muted transition-colors hover:text-[color:var(--primary-ink)]"
                  >
                    {formatLong(d.date)}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>

      <aside className="flex flex-col gap-8 lg:sticky lg:top-20 lg:self-start">
        <Toc items={toc} />
        {related.length > 0 && (
          <div className="text-sm">
            <p className="mb-3 font-mono text-xs uppercase tracking-wider text-faint">
              Vedi anche
            </p>
            <ul className="flex flex-col gap-1.5">
              {related.map((c) => (
                <li key={c.slug}>
                  <Link
                    href={`/kb/${c.slug}`}
                    className="text-muted transition-colors hover:text-[color:var(--primary-ink)]"
                  >
                    {c.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
        {capitoli.length > 0 && (
          <div className="text-sm">
            <p className="mb-3 font-mono text-xs uppercase tracking-wider text-faint">
              Nei Fondamenti di AI
            </p>
            <ul className="flex flex-col gap-1.5">
              {capitoli.map((c) => (
                <li key={c.slug}>
                  <Link
                    href={`/fondamenti/${c.slug}`}
                    className="text-muted transition-colors hover:text-[color:var(--primary-ink)]"
                  >
                    Cap. {c.capitolo} — {c.titolo}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </aside>
    </div>
  );
}
