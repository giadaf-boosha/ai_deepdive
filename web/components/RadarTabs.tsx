"use client";

import { useMemo, useState } from "react";
import type { App, Benchmark, CatalogTool, Model, ModelId, ModelsData, UseRow } from "@/lib/models";
import { ModelCard } from "./ModelCard";
import { ArrowUpRight } from "./Icons";

const BRAND: Record<ModelId, string> = {
  claude: "#e8901b",
  chatgpt: "#0f766e",
  gemini: "#2563eb",
};

const TABS = ["Modelli", "App di testo", "Tools per categoria", "Cosa usare per cosa", "Benchmark"] as const;
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
      {tab === "App di testo" && <AppsPanel apps={data.apps} />}
      {tab === "Tools per categoria" && <ToolsPanel tools={data.tools} />}
      {tab === "Cosa usare per cosa" && <MatrixPanel rows={data.useMatrix} />}
      {tab === "Benchmark" && <BenchmarkPanel benchmarks={data.benchmarks} nameById={nameById} />}
    </div>
  );
}

function ModelsPanel({ models }: { models: Model[] }) {
  return (
    <div className="flex flex-col gap-5">
      <p className="max-w-prose text-sm text-muted">
        Il <span className="text-ink">modello</span> e&apos; il motore (es. Claude Opus 4.8);
        l&apos;<span className="text-ink">app</span> e&apos; il prodotto che lo usa (es. Claude.ai).
        Qui i modelli di frontiera a confronto sul piano tecnico — le app nella tab accanto.
      </p>
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        {models.map((m) => (
          <ModelCard key={m.id} model={m} />
        ))}
      </div>
    </div>
  );
}

function AppsPanel({ apps }: { apps: App[] }) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      {apps.map((app) => (
        <article key={app.id} className="card flex flex-col gap-3 p-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h3 className="text-base font-semibold text-ink">{app.name}</h3>
              <p className="font-mono text-xs text-faint">{app.provider} · {app.poweredBy}</p>
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
          <p className="text-sm leading-relaxed text-muted">{app.tagline}</p>
          <div className="flex flex-wrap gap-1.5">
            {app.features.map((f) => (
              <span key={f} className="chip text-xs">{f}</span>
            ))}
          </div>
          <dl className="mt-1 flex flex-col gap-1 border-t border-line pt-3 text-xs">
            <div className="flex justify-between gap-3">
              <dt className="text-faint">Free</dt>
              <dd className="text-right text-muted">{app.pricingFree}</dd>
            </div>
            <div className="flex justify-between gap-3">
              <dt className="text-faint">A pagamento</dt>
              <dd className="text-right font-medium text-ink">{app.pricingPaid}</dd>
            </div>
          </dl>
        </article>
      ))}
    </div>
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
                  <span className="flex items-center justify-between gap-2">
                    <span className="text-sm font-semibold text-ink">{t.name}</span>
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
                          className="rounded-full bg-primary/10 px-2.5 py-0.5 text-sm font-medium text-[color:var(--primary-ink)]"
                        >
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
  nameById,
}: {
  benchmarks: Benchmark[];
  nameById: Map<ModelId, string>;
}) {
  return (
    <div className="flex flex-col gap-8">
      <p className="max-w-prose text-sm text-muted">
        Benchmark non confrontabili tra loro. SWE-Bench Pro, Computer Use e GPQA Diamond sono
        percentuali (piu&apos; alto = meglio); per LMArena il valore e&apos; una posizione in classifica
        (piu&apos; basso = meglio).
      </p>
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
                        style={{ width: `${Math.max(width, 14)}%`, backgroundColor: BRAND[s.modelId] }}
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

function CatBtn({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
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
