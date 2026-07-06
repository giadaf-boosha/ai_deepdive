import type { Model } from "@/lib/models";
import { brandColor } from "@/lib/brand";
import { Logo } from "./Logo";

export function ModelCardCompact({ model }: { model: Model }) {
  return (
    <div className="card card-hover flex flex-col gap-2 p-5">
      <div className="flex items-center gap-2.5">
        <Logo domain={model.domain} name={model.name} size={22} />
        <span className="text-sm font-semibold text-ink">{model.name}</span>
      </div>
      <p className="font-mono text-xs text-faint">{model.provider}</p>
      <p className="text-sm leading-relaxed text-muted">{model.tagline ?? model.verdict}</p>
    </div>
  );
}

export function ModelCard({ model }: { model: Model }) {
  return (
    <article
      className="card flex h-full flex-col gap-4 p-6"
      style={{ borderTopColor: brandColor(model.id), borderTopWidth: 3 }}
    >
      <header className="flex flex-col gap-1">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2.5">
            <Logo domain={model.domain} name={model.name} size={24} />
            <h3 className="text-lg font-semibold leading-tight text-ink">{model.name}</h3>
          </div>
          <span className="chip shrink-0">{model.provider}</span>
        </div>
        <p className="mt-1 font-mono text-xs text-faint">rilascio {model.releaseDate}</p>
        {model.tagline && <p className="mt-1 text-sm text-muted">{model.tagline}</p>}
      </header>

      <Block title="Punti di forza" items={model.strengths} tone="pos" />
      <Block title="Limiti" items={model.weaknesses} tone="neg" />
      <Block title="Ideale per" items={model.bestFor} tone="neutral" />

      <div className="mt-auto rounded-lg border border-line bg-paper p-3">
        <p className="mb-1 font-mono text-xs uppercase tracking-wider text-faint">Verdetto</p>
        <p className="text-sm text-ink">{model.verdict}</p>
      </div>

      <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-muted">
        <Stat label="Context" value={model.contextWindow} />
        <Stat label="LMArena" value={model.lmarenaRank > 0 ? `#${model.lmarenaRank}` : "n/d"} />
        <Stat
          label="API in/out"
          value={model.apiInputPer1M > 0 ? `$${model.apiInputPer1M}/$${model.apiOutputPer1M}` : "open / n/d"}
        />
        <Stat label="Multimodale" value={model.supportsImages ? "si" : "solo testo"} />
      </dl>
    </article>
  );
}

function Block({ title, items, tone }: { title: string; items: string[]; tone: "pos" | "neg" | "neutral" }) {
  if (!items?.length) return null;
  const marker = tone === "pos" ? "text-cat-modelli" : tone === "neg" ? "text-cat-business" : "text-faint";
  return (
    <div>
      <p className="mb-1.5 font-mono text-xs uppercase tracking-wider text-faint">{title}</p>
      <ul className="flex flex-col gap-1 text-sm text-muted">
        {items.map((item) => (
          <li key={item} className="flex gap-2">
            <span className={`mt-1 ${marker}`} aria-hidden>•</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-baseline justify-between gap-2 border-b border-line py-1 last:border-0">
      <dt className="text-faint">{label}</dt>
      <dd className="font-medium text-ink">{value}</dd>
    </div>
  );
}
