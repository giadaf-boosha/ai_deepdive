import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  getChapterBySlug,
  getChapterSlugs,
  getAdjacentChapters,
  parteByNumero,
} from "@/lib/fondamenti";
import { kbConceptsInChapter } from "@/lib/relations";
import { extractToc, stripLeadingH1 } from "@/lib/markdown";
import { MarkdownContent } from "@/components/MarkdownContent";
import { Toc } from "@/components/Toc";

export const dynamicParams = false;

export function generateStaticParams() {
  return getChapterSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const cap = getChapterBySlug(slug);
  if (!cap) return { title: "Capitolo non trovato" };
  return {
    title: `${cap.titolo} — Fondamenti di AI`,
    description: cap.excerpt,
  };
}

export default async function CapitoloPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const cap = getChapterBySlug(slug);
  if (!cap) notFound();

  const body = stripLeadingH1(cap.content);
  const toc = extractToc(body);
  const { prev, next } = getAdjacentChapters(slug);
  const parte = parteByNumero(cap.parte);
  const concetti = kbConceptsInChapter(cap);

  return (
    <div className="container-wide grid grid-cols-1 gap-10 lg:grid-cols-[1fr_16rem]">
      <div className="flex min-w-0 flex-col gap-8">
        <div>
          <Link href="/fondamenti" className="link-primary text-sm">
            ← Fondamenti di AI
          </Link>
        </div>

        <header className="flex flex-col gap-3 border-b border-line pb-5">
          <div className="flex flex-wrap items-center gap-2">
            {parte && (
              <span className="chip">
                Parte {parte.numero} — {parte.titolo}
              </span>
            )}
            <span className="font-mono text-xs text-faint">
              Capitolo {cap.capitolo}
            </span>
          </div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            {cap.titolo}
          </h1>
        </header>

        <article>
          <MarkdownContent content={body} rewriteFondamenti />
        </article>

        <nav className="flex items-stretch justify-between gap-4 border-t border-line pt-6">
          {prev ? (
            <Link
              href={`/fondamenti/${prev.slug}`}
              className="group flex flex-col gap-1 text-sm"
            >
              <span className="text-faint">← Capitolo {prev.capitolo}</span>
              <span className="font-medium text-muted group-hover:text-[color:var(--primary-ink)]">
                {prev.titolo}
              </span>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link
              href={`/fondamenti/${next.slug}`}
              className="group flex flex-col items-end gap-1 text-right text-sm"
            >
              <span className="text-faint">Capitolo {next.capitolo} →</span>
              <span className="font-medium text-muted group-hover:text-[color:var(--primary-ink)]">
                {next.titolo}
              </span>
            </Link>
          ) : (
            <span />
          )}
        </nav>
      </div>

      <aside className="flex flex-col gap-8 lg:sticky lg:top-20 lg:self-start">
        <Toc items={toc} />
        {concetti.length > 0 && (
          <div className="text-sm">
            <p className="mb-3 font-mono text-xs uppercase tracking-wider text-faint">
              Nella knowledge base
            </p>
            <ul className="flex flex-col gap-1.5">
              {concetti.map((c) => (
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
      </aside>
    </div>
  );
}
