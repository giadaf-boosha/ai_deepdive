import type { NextConfig } from "next";
import path from "node:path";

// Il layer web legge i markdown da ../digest e ../kb a build time (SSG).
// outputFileTracingRoot punta alla root del repo cosi' il tracing dei file
// considera correttamente i contenuti fuori dalla cartella web/.
const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(process.cwd(), ".."),
  eslint: {
    // La qualita' del codice e' garantita da `tsc --noEmit`; il lint non blocca il build su Vercel.
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
