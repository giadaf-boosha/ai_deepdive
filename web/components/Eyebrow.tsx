// Eyebrow Boosha: monospace uppercase con quadratino arancione (firma del brand).
export function Eyebrow({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <p className={`eyebrow ${className}`}>{children}</p>;
}
