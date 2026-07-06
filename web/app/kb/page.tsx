import type { Metadata } from "next";
import { getAllConcepts, getCategories, toCardData } from "@/lib/kb";
import { KBIndex } from "@/components/KBIndex";
import { Eyebrow } from "@/components/Eyebrow";

export const metadata: Metadata = {
  title: "Knowledge base",
  description:
    "Concetti tecnici AI raccontati in italiano: deep dive aggiornati dai digest giornalieri.",
};

export default function KBPage() {
  const concepts = getAllConcepts().map(toCardData);
  const categories = getCategories();

  return (
    <div className="container-wide flex flex-col gap-8 pt-4">
      <header className="flex flex-col gap-3">
        <Eyebrow>Concetti spiegati</Eyebrow>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Knowledge base</h1>
        <p className="max-w-prose text-lg text-muted">
          {concepts.length} concetti documentati. Deep dive in italiano, nomi
          tecnici inalterati.
        </p>
      </header>
      <KBIndex concepts={concepts} categories={categories} />
    </div>
  );
}
