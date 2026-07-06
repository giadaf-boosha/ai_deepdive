import data from "@/data/models.json";

export type ModelId = string;
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
  tagline?: string;
  contextWindow: string;
  apiInputPer1M: number;
  apiOutputPer1M: number;
  supportsImages: boolean;
  supportsVideo: boolean;
  supportsCode: boolean;
  supportsAgents: boolean;
  privacyRating?: PrivacyRating;
  enterpriseCertifications?: string[];
  dataResidency?: string;
  trainingPolicy?: string;
  strengths: string[];
  weaknesses: string[];
  bestFor: string[];
  verdict: string;
  lmarenaRank: number;
  domain: string;
}

// App/prodotto (scheda tool): cosa fa, funzionalita, tier, caveat, sweet spot.
export interface App {
  id: string;
  name: string;
  url: string;
  provider: string;
  poweredBy?: string;
  cosaFa: string;
  funzionalita: string[];
  tierGratuito: string;
  caveat: string;
  sweetSpot: string;
}

export interface CatalogTool {
  category: ToolCategory;
  name: string;
  url: string;
  oneLiner: string;
}

export interface UseRow {
  category: string;
  task: string;
  recommended: string[];
  why: string;
}

// Tabella comparativa dei "contenitori" (assistenti con knowledge base).
export interface ContainerRow {
  dimensione: string;
  customGpts: string;
  chatgptProjects: string;
  claudeProjects: string;
  geminiGems: string;
  perplexitySpaces: string;
}

export interface DecisionRow {
  scenario: string;
  tool: string;
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

export interface LinkRef {
  name: string;
  url: string;
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
  benchmarkLinks: LinkRef[];
}

export interface ModelsData {
  meta: ModelsMeta;
  models: Model[];
  apps: App[];
  tools: CatalogTool[];
  useMatrix: UseRow[];
  containers: ContainerRow[];
  decisionTree: DecisionRow[];
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
