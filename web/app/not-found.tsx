import Link from "next/link";

export default function NotFound() {
  return (
    <div className="container-prose flex flex-col items-start gap-4 py-20">
      <p className="font-mono text-sm text-accent">404</p>
      <h1 className="text-3xl font-semibold tracking-tight">Pagina non trovata</h1>
      <p className="text-muted">
        Il contenuto richiesto non esiste o e&apos; stato spostato.
      </p>
      <Link href="/" className="link-primary">
        ← Torna alla home
      </Link>
    </div>
  );
}
