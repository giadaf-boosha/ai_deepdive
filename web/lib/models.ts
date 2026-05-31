import modelsData from "@/data/models.json";

export type ModelId = "claude" | "chatgpt" | "gemini" | "copilot";
export type PrivacyRating = "high" | "medium" | "low";

export interface ModelPricing {
  free: string;
  pro: string;
  proPrice: number;
  team: string;
  enterprise: string;
  apiInputPer1M: number;
  apiOutputPer1M: number;
}

export interface Model {
  id: ModelId;
  provider: string;
  name: string;
  latestModel: string;
  releaseDate: string;
  tagline: string;
  strengths: string[];
  weaknesses: string[];
  bestFor: string[];
  pricing: ModelPricing;
  contextWindow: string;
  supportsImages: boolean;
  supportsVideo: boolean;
  supportsCode: boolean;
  supportsAgents: boolean;
  privacyRating: PrivacyRating;
  enterpriseCertifications: string[];
  dataResidency: string;
  trainingPolicy: string;
  verdict: string;
  lmarenaRank: number;
  lmarenaFinancialRank: number;
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

export interface UseCaseRating {
  modelId: ModelId;
  rating: number; // 1-5
}

export interface UseCase {
  category: string;
  task: string;
  ratings: UseCaseRating[];
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
  benchmarks: Benchmark[];
  useCases: UseCase[];
  changelog: ChangelogEntry[];
}

const data = modelsData as ModelsData;

export function getModelsData(): ModelsData {
  return data;
}

export function getModels(): Model[] {
  return data.models;
}

export function getModelById(id: ModelId): Model | undefined {
  return data.models.find((m) => m.id === id);
}

export function getUseCaseCategories(): string[] {
  return Array.from(new Set(data.useCases.map((u) => u.category)));
}
