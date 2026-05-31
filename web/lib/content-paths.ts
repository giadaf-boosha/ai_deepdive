import path from "node:path";

// La cartella web/ vive dentro il repo ai_deepdive. A build time leggiamo i
// markdown da ../digest e ../kb rispetto alla root del repo.
export const REPO_ROOT = path.join(process.cwd(), "..");
export const DIGEST_DIR = path.join(REPO_ROOT, "digest");
export const KB_DIR = path.join(REPO_ROOT, "kb", "concetti");
