"use client";

import { useMemo, useState } from "react";
import type {
  Benchmark,
  Model,
  ModelId,
  ModelsData,
  UseCase,
} from "@/lib/models";
import { ModelCard } from "./ModelCard";

const BRAND: Record<ModelId, string> = {
  claude: "#e8901b",
  chatgpt: "#0f766e",
  gemini: "#2563eb",
  copilot: "#7c3aed",
};

const TABS = [
  "Panoramica",
  "Benchmark",
  "Casi d'uso",
  "Prezzi",
  "Privacy & enterprise",
] as const;

type Tab = (typeof TABS)[number];

export function RadarTabs({ data }: { data: ModelsData }) {
  const [tab, setTab] = useState<Tab>("Panoramica");
  const nameById = useMemo(() => {
    const map = new Map<ModelId, string>();
    for (const m of data.models) map.set(m.id, m.name);
    return map;
  }, [data.models]);

  return (
    <div className="flex flex-col gap-8">
      <div
        role="tablist"
        className="-mx-5 flex gap-1 overflow-x-auto border-b border-line px-5 sm:mx-0 sm:px-0"
      >
        {TABS.map((t) => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            className={`-mb-px shrink-0 whitespace-nowrap border-b-2 px-3.5 py-2.5 text-sm font-medium transition-colors sm:px-4 ${
              tab === t
                ? "border-accent text-ink"
                : "border-transparent text-muted hover:text-ink"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Panoramica" && (
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
          {data.models.map((m) => (
            <ModelCard key={m.id} model={m} />
          ))}
        </div>
      )}

      {tab === "Benchmark" && (
        <BenchmarkPanel benchmarks={data.benchmarks} nameById={nameById} />
      )}

      {tab === "Casi d'uso" && (
        <UseCasePanel useCases={data.useCases} models={data.models} />
      )}

      {tab === "Prezzi" && <PricingPanel models={data.models} />}

      {tab === "Privacy & enterprise" && <PrivacyPanel models={data.models} />}
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
        I benchmark misurano dimensioni diverse e non sono direttamente
        confrontabili tra loro. SWE-Bench Pro, Computer Use (OSWorld) e GPQA
        Diamond sono punteggi percentuali (piu' alto = meglio). Per LMArena il
        valore e' una posizione in classifica (piu' basso = meglio).
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
                const width = b.lowerIsBetter
                  ? ((max + 1 - s.value) / max) * 100
                  : (s.value / max) * 100;
                return (
                  <div key={s.modelId} className="flex items-center gap-3">
                    <span className="w-28 shrink-0 text-sm text-muted">
                      {nameById.get(s.modelId) ?? s.modelId}
                    </span>
                    <div className="h-6 flex-1 overflow-hidden rounded bg-paper">
                      <div
                        className="flex h-full items-center justify-end rounded px-2 text-xs font-medium text-white"
                        style={{
                          width: `${Math.max(width, 12)}%`,
                          backgroundColor: BRAND[s.modelId],
                        }}
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

function UseCasePanel({
  useCases,
  models,
}: {
  useCases: UseCase[];
  models: Model[];
}) {
  const categories = useMemo(
    () => Array.from(new Set(useCases.map((u) => u.category))),
    [useCases],
  );
  const [category, setCategory] = useState("all");
  const rows = useCases.filter((u) => category === "all" || u.category === category);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-1.5">
        <CatBtn active={category === "all"} onClick={() => setCategory("all")}>
          Tutte
        </CatBtn>
        {categories.map((c) => (
          <CatBtn key={c} active={category === c} onClick={() => setCategory(c)}>
            {c}
          </CatBtn>
        ))}
      </div>
      <div className="overflow-x-auto rounded-lg border border-line">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-line bg-surface text-left">
              <th className="px-4 py-3 font-medium text-muted">Caso d&apos;uso</th>
              {models.map((m) => (
                <th key={m.id} className="px-3 py-3 text-center font-medium text-muted">
                  {m.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((u) => (
              <tr key={`${u.category}-${u.task}`} className="border-b border-line last:border-0">
                <td className="px-4 py-3">
                  <span className="block text-ink">{u.task}</span>
                  <span className="font-mono text-xs text-faint">{u.category}</span>
                </td>
                {models.map((m) => {
                  const r = u.ratings.find((x) => x.modelId === m.id);
                  return (
                    <td key={m.id} className="px-3 py-3 text-center">
                      <Rating value={r?.rating ?? 0} color={BRAND[m.id]} />
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-faint">
        Valutazione 1–5 basata su benchmark pubblici e posizionamento dichiarato.
        Indicativa, non sostituisce un test sul caso d&apos;uso reale.
      </p>
    </div>
  );
}

function Rating({ value, color }: { value: number; color: string }) {
  return (
    <span className="inline-flex gap-0.5" title={`${value}/5`}>
      {[1, 2, 3, 4, 5].map((i) => (
        <span
          key={i}
          className="h-1.5 w-1.5 rounded-full"
          style={{ backgroundColor: i <= value ? color : "var(--line)" }}
        />
      ))}
    </span>
  );
}

function PricingPanel({ models }: { models: Model[] }) {
  return (
    <div className="flex flex-col gap-4">
      <div className="overflow-x-auto rounded-lg border border-line">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-line bg-surface text-left">
              <th className="px-4 py-3 font-medium text-muted">Modello</th>
              <th className="px-4 py-3 font-medium text-muted">Free</th>
              <th className="px-4 py-3 font-medium text-muted">Pro / Plus</th>
              <th className="px-4 py-3 font-medium text-muted">Team</th>
              <th className="px-4 py-3 font-medium text-muted">Enterprise</th>
              <th className="px-4 py-3 font-medium text-muted">API /1M (in/out)</th>
            </tr>
          </thead>
          <tbody>
            {models.map((m) => (
              <tr key={m.id} className="border-b border-line align-top last:border-0">
                <td className="px-4 py-3 font-medium text-ink">{m.name}</td>
                <td className="px-4 py-3 text-muted">{m.pricing.free}</td>
                <td className="px-4 py-3 text-muted">{m.pricing.pro}</td>
                <td className="px-4 py-3 text-muted">{m.pricing.team}</td>
                <td className="px-4 py-3 text-muted">{m.pricing.enterprise}</td>
                <td className="px-4 py-3 font-mono text-xs text-ink">
                  {m.pricing.apiInputPer1M > 0
                    ? `$${m.pricing.apiInputPer1M} / $${m.pricing.apiOutputPer1M}`
                    : "n/d"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-faint">
        Prezzi in USD da fonti ufficiali dei vendor. I piani consumer e i prezzi
        API cambiano frequentemente: verificare sempre la pagina pricing ufficiale.
      </p>
    </div>
  );
}

function PrivacyPanel({ models }: { models: Model[] }) {
  return (
    <div className="overflow-x-auto rounded-lg border border-line">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-line bg-surface text-left">
            <th className="px-4 py-3 font-medium text-muted">Modello</th>
            <th className="px-4 py-3 font-medium text-muted">Privacy</th>
            <th className="px-4 py-3 font-medium text-muted">Certificazioni</th>
            <th className="px-4 py-3 font-medium text-muted">Data residency</th>
            <th className="px-4 py-3 font-medium text-muted">Politica training</th>
          </tr>
        </thead>
        <tbody>
          {models.map((m) => (
            <tr key={m.id} className="border-b border-line align-top last:border-0">
              <td className="px-4 py-3 font-medium text-ink">{m.name}</td>
              <td className="px-4 py-3">
                <span className="chip capitalize">{m.privacyRating}</span>
              </td>
              <td className="px-4 py-3">
                <div className="flex flex-wrap gap-1">
                  {m.enterpriseCertifications.map((c) => (
                    <span key={c} className="chip text-xs">
                      {c}
                    </span>
                  ))}
                </div>
              </td>
              <td className="px-4 py-3 text-muted">{m.dataResidency}</td>
              <td className="px-4 py-3 text-muted">{m.trainingPolicy}</td>
            </tr>
          ))}
        </tbody>
      </table>
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
        active
          ? "border-accent bg-accent text-accent-fg"
          : "border-line text-muted hover:border-accent/50 hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}
