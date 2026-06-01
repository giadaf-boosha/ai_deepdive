import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllDocs, getDocBySlug, getDocSlugs } from "@/lib/claudecode";
import { extractToc } from "@/lib/markdown";
import { MarkdownContent } from "@/components/MarkdownContent";
import { Toc } from "@/components/Toc";
import { Eyebrow } from "@/components/Eyebrow";
import { ArrowUpRight } from "@/components/Icons";

export const dynamicParams = false;

export function generateStaticParams() {
  return getDocSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const doc = getDocBySlug(slug);
  if (!doc) return { title: "Capitolo non trovato" };
  return { title: `${doc.title} · Claude Code`, description: doc.excerpt };
}

export default async function ClaudeCodeDocPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const doc = getDocBySlug(slug);
  if (!doc) notFound();

  const toc = extractToc(doc.content);
  const docs = getAllDocs();
  const idx = docs.findIndex((d) => d.slug === slug);
  const prev = idx > 0 ? docs[idx - 1] : null;
  const next = idx < docs.length - 1 ? docs[idx + 1] : null;

  return (
    <div className="container-wide grid grid-cols-1 gap-10 pt-4 lg:grid-cols-[1fr_16rem]">
      <div className="flex min-w-0 flex-col gap-8">
        <div>
          <Link href="/claude-code" className="link-primary text-sm">
            ← Guida Claude Code
          </Link>
        </div>

        <header className="flex flex-col gap-3 border-b border-line pb-5">
          <Eyebrow>Capitolo</Eyebrow>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{doc.title}</h1>
          <a
            href={doc.source}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 font-mono text-xs text-faint hover:text-[color:var(--primary-ink)]"
          >
            sorgente su GitHub <ArrowUpRight className="h-3.5 w-3.5" />
          </a>
        </header>

        <article>
          <MarkdownContent content={doc.content} />
        </article>

        <nav className="flex items-stretch justify-between gap-4 border-t border-line pt-6">
          {prev ? (
            <Link href={`/claude-code/${prev.slug}`} className="group flex flex-col gap-1 text-sm">
              <span className="text-faint">← Precedente</span>
              <span className="font-medium text-muted group-hover:text-[color:var(--primary-ink)]">
                {prev.title}
              </span>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link
              href={`/claude-code/${next.slug}`}
              className="group flex flex-col items-end gap-1 text-right text-sm"
            >
              <span className="text-faint">Successivo →</span>
              <span className="font-medium text-muted group-hover:text-[color:var(--primary-ink)]">
                {next.title}
              </span>
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </div>

      <aside className="lg:sticky lg:top-20 lg:self-start">
        <Toc items={toc} />
      </aside>
    </div>
  );
}
