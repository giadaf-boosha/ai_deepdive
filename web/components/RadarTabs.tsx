"use client";

import { useMemo, useState } from "react";
import type {
  App,
  Benchmark,
  CatalogTool,
  ContainerRow,
  DecisionRow,
  LinkRef,
  Model,
  ModelId,
  ModelsData,
  UseRow,
} from "@/lib/models";
import { brandColor } from "@/lib/brand";
import { ModelCard } from "./ModelCard";
import { Logo } from "./Logo";
import { ArrowUpRight } from "./Icons";

// Domini per i loghi nei chip "consigliati" della matrice.
const NAME_DOMAINS: Record<string, string> = {
  Claude: "claude.ai",
  "Claude Code": "claude.com",
  ChatGPT: "chatgpt.com",
  "OpenAI Codex": "openai.com",
  Gemini: "gemini.google.com",
  Perplexity: "perplexity.ai",
  Grok: "grok.com",
  NotebookLM: "notebooklm.google.com",
  "Microsoft Copilot": "copilot.microsoft.com",
  Copilot: "copilot.microsoft.com",
  Gamma: "gamma.app",
  Midjourney: "midjourney.com",
  Ideogram: "ideogram.ai",
  "Adobe Firefly": "adobe.com",
  Canva: "canva.com",
  Sora: "sora.com",
  Runway: "runwayml.com",
  HeyGen: "heygen.com",
  "Opus Clip": "opus.pro",
  ElevenLabs: "elevenlabs.io",
  Suno: "suno.com",
  Zapier: "zapier.com",
  n8n: "n8n.io",
  Cursor: "cursor.com",
  Lovable: "lovable.dev",
  "Transcript LOL": "transcript.lol",
};
function domainFor(name: string): string | undefined {
  if (NAME_DOMAINS[name]) return NAME_DOMAINS[name];
  const hit = Object.keys(NAME_DOMAINS).find(
    (k) => name.toLowerCase().includes(k.toLowerCase()) || k.toLowerCase().includes(name.toLowerCase()),
  );
  return hit ? NAME_DOMAINS[hit] : undefined;
}

const TABS = ["Modelli", "App e tool", "Tools per categoria", "Cosa usare per cosa", "Benchmark"] as const;
type Tab = (typeof TABS)[number];

export function RadarTabs({ data }: { data: ModelsData }) {
  const [tab, setTab] = useState<Tab>("Cosa usare per cosa");
  const nameById = useMemo(() => {
    const m = new Map<ModelId, string>();
    for (const x of data.models) m.set(x.id, x.name);
    return m;
  }, [data.models]);

  return (
    <div className="flex flex-col gap-8">
      <div
        role="tablist"
        className="-mx-5 flex gap-1 overflow-x-auto border-b border-line px-5 sm:mx-0 sm:px-0 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
      >
        {TABS.map((t) => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            className={`-mb-px shrink-0 whitespace-nowrap border-b-2 px-3.5 py-2.5 text-sm font-medium transition-colors sm:px-4 ${
              tab === t ? "border-primary text-ink" : "border-transparent text-muted hover:text-ink"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Modelli" && <ModelsPanel models={data.models} />}
      {tab === "App e tool" && (
        <AppsPanel apps={data.apps} containers={data.containers} decisionTree={data.decisionTree} />
      )}
      {tab === "Tools per categoria" && <ToolsPanel tools={data.tools} />}
      {tab === "Cosa usare per cosa" && <MatrixPanel rows={data.useMatrix} />}
      {tab === "Benchmark" && (
        <BenchmarkPanel benchmarks={data.benchmarks} links={data.meta.benchmarkLinks} nameById={nameById} />
      )}
    </div>
  );
}

function ModelsPanel({ models }: { models: Model[] }) {
  return (
    <div className="flex flex-col gap-5">
      <p className="max-w-prose text-sm text-muted">
        Il <span className="text-ink">modello</span> e&apos; il motore (es. Claude Opus 4.8);
        l&apos;<span className="text-ink">app</span> e&apos; il prodotto che lo usa (es. Claude.ai).
        Qui {models.length} modelli di frontiera a confronto sul piano tecnico.
      </p>
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        {models.map((m) => (
          <ModelCard key={m.id} model={m} />
        ))}
      </div>
    </div>
  );
}

function AppsPanel({
  apps,
  containers,
  decisionTree,
}: {
  apps: App[];
  containers: ContainerRow[];
  decisionTree: DecisionRow[];
}) {
  return (
    <div className="flex flex-col gap-12">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {apps.map((app) => (
          <article key={app.id} className="card flex flex-col gap-3 p-5">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <Logo url={app.url} name={app.name} size={28} />
                <div>
                  <h3 className="text-base font-semibold leading-tight text-ink">{app.name}</h3>
                  <p className="font-mono text-[11px] text-faint">{app.provider}</p>
                </div>
              </div>
              <a
                href={app.url}
                target="_blank"
                rel="noreferrer"
                className="shrink-0 text-[color:var(--primary-ink)]"
                aria-label={`Apri ${app.name}`}
              >
                <ArrowUpRight className="h-4 w-4" />
              </a>
            </div>
            <p className="text-sm leading-relaxed text-muted">{app.cosaFa}</p>
            {app.funzionalita?.length > 0 && (
              <ul className="flex flex-col gap-1 text-sm text-muted">
                {app.funzionalita.slice(0, 6).map((f) => (
                  <li key={f} className="flex gap-2">
                    <span className="mt-1 text-[color:var(--primary-ink)]" aria-hidden>•</span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            )}
            <dl className="mt-1 flex flex-col gap-2 border-t border-line pt-3 text-xs">
              <Field label="Tier gratuito" value={app.tierGratuito} />
              <Field label="Caveat" value={app.caveat} />
              <Field label="Sweet spot" value={app.sweetSpot} accent />
            </dl>
          </article>
        ))}
      </div>

      {containers.length > 0 && <ContainersTable rows={containers} />}
      {decisionTree.length > 0 && <DecisionTree rows={decisionTree} />}
    </div>
  );
}

function Field({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  if (!value) return null;
  return (
    <div className="flex flex-col gap-0.5">
      <dt className="font-mono uppercase tracking-wider text-faint">{label}</dt>
      <dd className={accent ? "text-[color:var(--primary-ink)]" : "text-muted"}>{value}</dd>
    </div>
  );
}

const CONTAINER_COLS: { key: keyof ContainerRow; label: string; domain?: string }[] = [
  { key: "customGpts", label: "Custom GPT", domain: "chatgpt.com" },
  { key: "chatgptProjects", label: "ChatGPT Projects", domain: "chatgpt.com" },
  { key: "claudeProjects", label: "Claude Projects", domain: "claude.ai" },
  { key: "geminiGems", label: "Gemini Gems", domain: "gemini.google.com" },
  { key: "perplexitySpaces", label: "Perplexity Spaces", domain: "perplexity.ai" },
];

function ContainersTable({ rows }: { rows: ContainerRow[] }) {
  return (
    <section className="flex flex-col gap-4">
      <div>
        <h3 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">
          Contenitori a confronto
        </h3>
        <p className="mt-1 text-sm text-muted">
          Le piattaforme per costruire un assistente con knowledge base allegata: stesso concetto,
          declinazioni diverse.
        </p>
      </div>
      <div className="overflow-x-auto rounded-2xl border border-line">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-line bg-surface text-left">
              <th className="px-4 py-3 font-medium text-muted">Dimensione</th>
              {CONTAINER_COLS.map((c) => (
                <th key={c.key} className="px-4 py-3 font-medium text-ink">
                  <span className="flex items-center gap-1.5">
                    <Logo domain={c.domain} name={c.label} size={16} />
                    {c.label}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.dimensione} className="border-b border-line align-top last:border-0">
                <td className="px-4 py-3 font-medium text-ink">{r.dimensione}</td>
                {CONTAINER_COLS.map((c) => (
                  <td key={c.key} className="px-4 py-3 text-muted">{r[c.key]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function DecisionTree({ rows }: { rows: DecisionRow[] }) {
  return (
    <section className="flex flex-col gap-4">
      <h3 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">
        Quale contenitore scegliere
      </h3>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        {rows.map((r) => (
          <div key={r.scenario} className="card flex items-start gap-3 p-4">
            <span className="mt-0.5 shrink-0 text-[color:var(--primary-ink)]" aria-hidden>→</span>
            <div>
              <p className="text-sm text-ink">{r.scenario}</p>
              <p className="mt-1 inline-flex items-center gap-1.5 text-sm font-medium text-[color:var(--primary-ink)]">
                {domainFor(r.tool) && <Logo domain={domainFor(r.tool)} name={r.tool} size={16} />}
                {r.tool}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function ToolsPanel({ tools }: { tools: CatalogTool[] }) {
  const grouped = useMemo(() => {
    const out: Record<string, CatalogTool[]> = {};
    for (const t of tools) (out[t.category] ??= []).push(t);
    return out;
  }, [tools]);
  const order = ["Immagini", "Video", "Audio", "Agent", "Coding"];
  return (
    <div className="flex flex-col gap-10">
      {order
        .filter((c) => grouped[c]?.length)
        .map((cat) => (
          <section key={cat} className="flex flex-col gap-4">
            <h3 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">
              {cat}
              <span className="ml-2 text-faint">{grouped[cat].length}</span>
            </h3>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {grouped[cat].map((t) => (
                <a
                  key={t.name}
                  href={t.url}
                  target="_blank"
                  rel="noreferrer"
                  className="card card-hover group flex flex-col gap-1.5 p-4"
                >
                  <span className="flex items-center gap-2">
                    <Logo url={t.url} name={t.name} size={20} />
                    <span className="flex-1 text-sm font-semibold leading-tight text-ink">{t.name}</span>
                    <ArrowUpRight className="h-3.5 w-3.5 shrink-0 text-faint group-hover:text-[color:var(--primary-ink)]" />
                  </span>
                  <span className="text-xs leading-relaxed text-muted">{t.oneLiner}</span>
                </a>
              ))}
            </div>
          </section>
        ))}
    </div>
  );
}

function MatrixPanel({ rows }: { rows: UseRow[] }) {
  const categories = useMemo(() => Array.from(new Set(rows.map((r) => r.category))), [rows]);
  const [cat, setCat] = useState("all");
  const visible = cat === "all" ? categories : [cat];
  return (
    <div className="flex flex-col gap-6">
      <p className="max-w-prose text-sm text-muted">
        Parti dal bisogno, non dallo strumento: scegli cosa vuoi fare e trovi subito con cosa
        conviene farlo, e perche&apos;.
      </p>
      <div className="flex flex-wrap gap-1.5">
        <CatBtn active={cat === "all"} onClick={() => setCat("all")}>Tutte</CatBtn>
        {categories.map((c) => (
          <CatBtn key={c} active={cat === c} onClick={() => setCat(c)}>{c}</CatBtn>
        ))}
      </div>
      <div className="flex flex-col gap-10">
        {visible.map((c) => (
          <section key={c} className="flex flex-col gap-4">
            <h3 className="font-mono text-sm font-semibold uppercase tracking-wider text-ink">{c}</h3>
            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              {rows
                .filter((r) => r.category === c)
                .map((r) => (
                  <div key={r.task} className="card flex flex-col gap-3 p-5">
                    <p className="text-[15px] font-medium leading-snug text-ink">{r.task}</p>
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="font-mono text-xs uppercase tracking-wider text-faint">Usa</span>
                      {r.recommended.map((t) => (
                        <span
                          key={t}
                          className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 px-2.5 py-0.5 text-sm font-medium text-[color:var(--primary-ink)]"
                        >
                          {domainFor(t) && <Logo domain={domainFor(t)} name={t} size={15} />}
                          {t}
                        </span>
                      ))}
                    </div>
                    <p className="text-sm leading-relaxed text-muted">{r.why}</p>
                  </div>
                ))}
            </div>
          </section>
        ))}
      </div>
      <p className="text-xs text-faint">
        Consigli indicativi su tool pubblici, per orientarti in fretta. Verifica sempre sul tuo caso reale.
      </p>
    </div>
  );
}

function BenchmarkPanel({
  benchmarks,
  links,
  nameById,
}: {
  benchmarks: Benchmark[];
  links: LinkRef[];
  nameById: Map<ModelId, string>;
}) {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-3">
        <p className="max-w-prose text-sm text-muted">
          Benchmark non confrontabili tra loro. SWE-Bench Pro, Computer Use e GPQA Diamond sono
          percentuali (piu&apos; alto = meglio); per LMArena il valore e&apos; una posizione (piu&apos; basso = meglio).
        </p>
        {links?.length > 0 && (
          <div className="flex flex-wrap gap-2">
            <span className="font-mono text-xs uppercase tracking-wider text-faint">Classifiche live:</span>
            {links.map((l) => (
              <a
                key={l.url}
                href={l.url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 rounded-full border border-line px-3 py-1 text-xs font-medium text-ink transition-colors hover:border-primary/50"
              >
                <Logo url={l.url} name={l.name} size={16} />
                {l.name}
                <ArrowUpRight className="h-3 w-3 text-faint" />
              </a>
            ))}
          </div>
        )}
      </div>
      {benchmarks.map((b) => {
        const max = Math.max(...b.scores.map((s) => s.value), 1);
        return (
          <div key={b.id} className="flex flex-col gap-3">
            <div>
              <h3 className="text-base font-semibold text-ink">{b.name}</h3>
              <p className="text-sm text-faint">{b.description}</p>
            </div>
            <div className="flex flex-col gap-2.5">
              {b.scores.map((s) => {
                const width = b.lowerIsBetter ? ((max + 1 - s.value) / max) * 100 : (s.value / max) * 100;
                return (
                  <div key={s.modelId} className="flex items-center gap-3">
                    <span className="w-28 shrink-0 text-sm text-muted">{nameById.get(s.modelId) ?? s.modelId}</span>
                    <div className="h-6 flex-1 overflow-hidden rounded bg-surface-alt">
                      <div
                        className="flex h-full items-center justify-end rounded px-2 text-xs font-medium text-white"
                        style={{ width: `${Math.max(width, 14)}%`, backgroundColor: brandColor(s.modelId) }}
                      >
                        {b.lowerIsBetter ? `#${s.value}` : `${s.value}${b.unit}`}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function CatBtn({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
        active ? "border-primary bg-primary text-primary-fg" : "border-line text-muted hover:border-primary/50 hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}
