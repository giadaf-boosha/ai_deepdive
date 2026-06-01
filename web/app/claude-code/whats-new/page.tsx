import type { Metadata } from "next";
import Link from "next/link";
import { getWhatsNew } from "@/lib/claudecode";
import { formatLong } from "@/lib/dates";
import { Eyebrow } from "@/components/Eyebrow";
import { MarkdownContent } from "@/components/MarkdownContent";

export const metadata: Metadata = {
  title: "What's new — Claude Code",
  description: "Archivio delle novità giornaliere su Claude Code.",
};

export default function WhatsNewPage() {
  const days = getWhatsNew();

  return (
    <div className="container-prose flex flex-col gap-8 pt-4">
      <div>
        <Link href="/claude-code" className="link-primary text-sm">
          ← Guida Claude Code
        </Link>
      </div>
      <header className="flex flex-col gap-3 border-b border-line pb-5">
        <Eyebrow>Claude Code</Eyebrow>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          What&apos;s new — archivio
        </h1>
        <p className="text-muted">
          Le novità su Claude Code delle ultime settimane, dalla routine
          giornaliera.
        </p>
      </header>

      <div className="flex flex-col gap-8">
        {days.map((day) => (
          <section key={day.date} className="flex flex-col gap-3 border-b border-line pb-8 last:border-0">
            <h2 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">
              {formatLong(day.date)}
            </h2>
            {day.hasNews ? (
              <MarkdownContent content={day.body} />
            ) : (
              <p className="text-sm text-faint">Nessuna novità significativa.</p>
            )}
          </section>
        ))}
        {days.length === 0 && (
          <p className="text-sm text-faint">Archivio non disponibile.</p>
        )}
      </div>
    </div>
  );
}
