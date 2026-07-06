"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/digest", label: "Digest", short: "Digest" },
  { href: "/kb", label: "Knowledge base", short: "KB" },
  { href: "/fondamenti", label: "Fondamenti di AI", short: "Fondamenti" },
  { href: "/radar", label: "Confronto AI", short: "Confronto" },
  { href: "/claude-code", label: "Claude Code", short: "Claude" },
];

const BOOSHA_URL = "https://boosha.it/";

export function Nav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-line bg-paper/80 backdrop-blur-xl">
      <nav className="container-wide flex h-16 items-center justify-between gap-3">
        <div className="flex shrink-0 items-center gap-2.5">
          <Link
            href="/"
            className="text-[15px] font-semibold tracking-tight text-ink"
            aria-label="AI Deep Dive — home"
          >
            AI Deep Dive<span className="text-accent">.</span>
          </Link>
          <a
            href={BOOSHA_URL}
            target="_blank"
            rel="noreferrer"
            className="hidden font-mono text-[10px] uppercase tracking-[0.2em] text-faint transition-colors hover:text-[color:var(--primary-ink)] lg:inline"
          >
            by Boosha
          </a>
        </div>

        <ul className="-mr-2 flex items-center gap-0.5 overflow-x-auto sm:gap-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {LINKS.map((link) => {
            const active =
              pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <li key={link.href} className="shrink-0">
                <Link
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={`relative block whitespace-nowrap rounded-lg px-2.5 py-2 text-sm transition-colors sm:px-3.5 ${
                    active ? "font-medium text-ink" : "text-muted hover:text-ink"
                  }`}
                >
                  <span className="sm:hidden">{link.short}</span>
                  <span className="hidden sm:inline">{link.label}</span>
                  <span
                    className={`absolute inset-x-2.5 -bottom-px h-0.5 rounded-full bg-primary transition-opacity sm:inset-x-3.5 ${
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
