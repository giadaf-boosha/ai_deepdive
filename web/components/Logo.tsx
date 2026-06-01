// Logo di un modello/app/tool: usa il favicon del dominio (servizio Google,
// affidabile e senza chiave). Server-safe (nessun hook). Fallback: niente.

function hostFromUrl(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return url.replace(/^https?:\/\//, "").replace(/^www\./, "").split("/")[0];
  }
}

export function Logo({
  url,
  domain,
  name,
  size = 22,
  className = "",
}: {
  url?: string;
  domain?: string;
  name?: string;
  size?: number;
  className?: string;
}) {
  const d = (domain ?? (url ? hostFromUrl(url) : "")).trim();
  if (!d) return null;
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={`https://www.google.com/s2/favicons?domain=${encodeURIComponent(d)}&sz=64`}
      alt={name ? `Logo ${name}` : ""}
      width={size}
      height={size}
      loading="lazy"
      className={`shrink-0 rounded-[5px] bg-white object-contain ring-1 ring-line ${className}`}
      style={{ width: size, height: size }}
    />
  );
}
