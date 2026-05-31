import type { Metadata } from "next";
import { getAllConcepts, getCategories, toCardData } from "@/lib/kb";
import { KBIndex } from "@/components/KBIndex";

export const metadata: Metadata = {
  title: "Knowledge base",
  description:
    "Concetti tecnici AI raccontati in italiano: deep dive aggiornati dai digest giornalieri.",
};

export default function KBPage() {
  const concepts = getAllConcepts().map(toCardData);
  const categories = getCategories();

  return (
    <div className="container-wide flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold tracking-tight">Knowledge base</h1>
        <p className="text-muted">
          {concepts.length} concetti documentati. Deep dive in italiano, nomi
          tecnici inalterati.
        </p>
      </header>
      <KBIndex concepts={concepts} categories={categories} />
    </div>
  );
}
