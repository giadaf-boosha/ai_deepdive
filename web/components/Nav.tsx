"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/digest", label: "Digest" },
  { href: "/kb", label: "Knowledge base" },
  { href: "/radar", label: "Radar" },
];

export function Nav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-line bg-paper/80 backdrop-blur-xl">
      <nav className="container-wide flex h-16 items-center justify-between gap-3">
        <Link
          href="/"
          className="group flex items-center gap-2.5"
          aria-label="AI Deep Dive — home"
        >
          <span className="text-[15px] font-semibold tracking-tight text-ink">
            AI Deep Dive
            <span className="text-accent">.</span>
          </span>
          <span className="hidden font-mono text-[10px] uppercase tracking-[0.2em] text-faint sm:inline">
            Boosha
          </span>
        </Link>

        <ul className="flex items-center gap-0.5 sm:gap-1">
          {LINKS.map((link) => {
            const active =
              pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={`relative block rounded-lg px-2.5 py-2 text-sm transition-colors sm:px-3.5 ${
                    active ? "font-medium text-ink" : "text-muted hover:text-ink"
                  }`}
                >
                  {link.label}
                  <span
                    className={`absolute inset-x-2.5 -bottom-px h-0.5 rounded-full bg-accent transition-opacity sm:inset-x-3.5 ${
                      active ? "opacity-100" : "opacity-0"
                    }`}
                    aria-hidden
                  />
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
