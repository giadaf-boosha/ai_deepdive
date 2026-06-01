#!/usr/bin/env node
// Sync dei contenuti della guida Claude Code (repo separato giadaf-boosha/claude-code)
// dentro ai_deepdive. Copia docs/*.md + whats-new-archive.md in web/content/claude-code/,
// iniettando frontmatter (title da H1) e riscrivendo i link relativi del repo sorgente
// verso le route del sito. Pensato per girare in CI/pre-build o manualmente; il contenuto
// risultante viene committato cosi' il build legge solo dal proprio repo.
//
// Uso: node scripts/sync-claude-code.mjs

import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const REPO = "https://github.com/giadaf-boosha/claude-code.git";
const OUT_DIR = path.join(process.cwd(), "content", "claude-code");
const DOCS_OUT = path.join(OUT_DIR, "docs");
const SOURCE_BASE = "https://github.com/giadaf-boosha/claude-code/blob/main";

function log(m) {
  process.stdout.write(`[sync-claude-code] ${m}\n`);
}

// Riscrive i link markdown relativi del repo claude-code verso il sito.
function rewriteLinks(md) {
  return md.replace(/\]\((?!https?:|#|mailto:)([^)]+)\)/g, (_m, target) => {
    const [rawPath, hash = ""] = target.split("#");
    const clean = rawPath.replace(/^\.?\//, "").replace(/^\.\.\//, "");
    // Link a un capitolo docs -> /claude-code/<slug>
    const docMatch = clean.match(/(?:docs\/)?([\w.-]+)\.md$/i);
    if (clean === "README.md" || clean === "../README.md" || /(^|\/)README\.md$/.test(clean)) {
      return `](/claude-code${hash ? "#" + hash : ""})`;
    }
    if (docMatch && /\.md$/i.test(clean)) {
      const slug = docMatch[1];
      if (slug === "whats-new-archive") return `](/claude-code/whats-new)`;
      return `](/claude-code/${slug}${hash ? "#" + hash : ""})`;
    }
    // Altri file del repo (skills/, spec.md, ecc.) -> link assoluto a GitHub.
    return `](${SOURCE_BASE}/${clean}${hash ? "#" + hash : ""})`;
  });
}

// Estrae il primo H1 come title e rimuove H1 + eventuale blockquote breadcrumb iniziale.
function extractTitleAndBody(md) {
  const lines = md.split("\n");
  let title = "";
  const out = [];
  let removedH1 = false;
  let skippingBreadcrumb = false;
  for (const line of lines) {
    if (!removedH1) {
      const h1 = /^#\s+(.*)$/.exec(line);
      if (h1) {
        title = h1[1].replace(/\s*#+\s*$/, "").trim();
        removedH1 = true;
        skippingBreadcrumb = true;
        continue;
      }
    }
    if (skippingBreadcrumb) {
      if (line.trim() === "") continue; // salta righe vuote tra H1 e breadcrumb
      if (line.trimStart().startsWith(">")) continue; // salta il blockquote breadcrumb
      skippingBreadcrumb = false;
    }
    out.push(line);
  }
  return { title, body: out.join("\n").trim() };
}

function yamlEscape(s) {
  return `"${String(s).replace(/"/g, '\\"')}"`;
}

function main() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "cc-sync-"));
  log(`clono ${REPO} (shallow) in ${tmp}`);
  execSync(`git clone --depth 1 ${REPO} "${tmp}"`, { stdio: "inherit" });

  const srcDocs = path.join(tmp, "docs");
  fs.rmSync(OUT_DIR, { recursive: true, force: true });
  fs.mkdirSync(DOCS_OUT, { recursive: true });

  const files = fs
    .readdirSync(srcDocs)
    .filter((f) => f.endsWith(".md") && f !== "whats-new-archive.md");

  let count = 0;
  for (const file of files) {
    const raw = fs.readFileSync(path.join(srcDocs, file), "utf-8");
    const { title, body } = extractTitleAndBody(raw);
    const slug = file.replace(/\.md$/, "");
    const order = (slug.match(/^(\d+)/)?.[1] ?? "99").padStart(3, "0");
    const fm = [
      "---",
      `title: ${yamlEscape(title || slug)}`,
      `slug: ${slug}`,
      `order: ${yamlEscape(order)}`,
      `source: ${SOURCE_BASE}/docs/${file}`,
      "---",
      "",
    ].join("\n");
    fs.writeFileSync(path.join(DOCS_OUT, file), fm + rewriteLinks(body) + "\n");
    count++;
  }

  // whats-new-archive.md: copiato con link riscritti, senza frontmatter (parsing dedicato).
  const archiveSrc = path.join(srcDocs, "whats-new-archive.md");
  if (fs.existsSync(archiveSrc)) {
    const raw = fs.readFileSync(archiveSrc, "utf-8");
    fs.writeFileSync(path.join(OUT_DIR, "whats-new-archive.md"), rewriteLinks(raw));
  }

  // Metadati di sync.
  fs.writeFileSync(
    path.join(OUT_DIR, "_sync.json"),
    JSON.stringify(
      { syncedFrom: REPO, docs: count, syncedAtNote: "vedi git log per la data" },
      null,
      2,
    ) + "\n",
  );

  fs.rmSync(tmp, { recursive: true, force: true });
  log(`completato: ${count} capitoli docs + whats-new-archive`);
}

main();
