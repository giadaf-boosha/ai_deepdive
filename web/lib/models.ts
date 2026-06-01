import data from "@/data/models.json";

export type ModelId = "claude" | "chatgpt" | "gemini";
export type PrivacyRating = "high" | "medium" | "low";
export type ToolCategory =
  | "Testo"
  | "Immagini"
  | "Video"
  | "Audio"
  | "Agent"
  | "Coding";

// Modello LLM sottostante (livello tecnico): benchmark, API, contesto.
export interface Model {
  id: ModelId;
  provider: string;
  name: string;
  releaseDate: string;
  tagline: string;
  contextWindow: string;
  apiInputPer1M: number;
  apiOutputPer1M: number;
  supportsImages: boolean;
  supportsVideo: boolean;
  supportsCode: boolean;
  supportsAgents: boolean;
  privacyRating: PrivacyRating;
  enterpriseCertifications: string[];
  dataResidency: string;
  trainingPolicy: string;
  strengths: string[];
  weaknesses: string[];
  bestFor: string[];
  verdict: string;
  lmarenaRank: number;
}

// App/prodotto consumer (livello prodotto): feature, prezzi consumer.
export interface App {
  id: string;
  name: string;
  url: string;
  provider: string;
  poweredBy: string;
  tagline: string;
  pricingFree: string;
  pricingPaid: string;
  features: string[];
  bestFor: string[];
}

// Tool del catalogo per categoria.
export interface CatalogTool {
  category: ToolCategory;
  name: string;
  url: string;
  oneLiner: string;
}

// Riga della matrice "cosa usare per cosa".
export interface UseRow {
  category: string;
  task: string;
  recommended: string[];
  why: string;
}

export interface BenchmarkScore {
  modelId: ModelId;
  value: number;
}
export interface Benchmark {
  id: string;
  name: string;
  description: string;
  unit: string;
  lowerIsBetter: boolean;
  scores: BenchmarkScore[];
}

export interface ChangelogEntry {
  date: string;
  summary: string;
  sources: string[];
}

export interface ModelsMeta {
  lastUpdated: string;
  generatedBy: string;
  sourcesChecked: string[];
  nextScheduledUpdate: string;
}

export interface ModelsData {
  meta: ModelsMeta;
  models: Model[];
  apps: App[];
  tools: CatalogTool[];
  useMatrix: UseRow[];
  benchmarks: Benchmark[];
  changelog: ChangelogEntry[];
}

const typed = data as ModelsData;

export function getModelsData(): ModelsData {
  return typed;
}
export function getModels(): Model[] {
  return typed.models;
}
export function getModelById(id: ModelId): Model | undefined {
  return typed.models.find((m) => m.id === id);
}
export function getApps(): App[] {
  return typed.apps;
}
export function getToolsByCategory(): Record<string, CatalogTool[]> {
  const out: Record<string, CatalogTool[]> = {};
  for (const t of typed.tools) (out[t.category] ??= []).push(t);
  return out;
}
