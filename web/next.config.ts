import type { NextConfig } from "next";

// Il layer web legge i markdown da ../digest e ../kb a build time (SSG puro:
// tutte le route hanno generateStaticParams, nessun runtime server).
// output: "export" produce un sito statico in web/out servibile da Vercel
// come progetto statico (framework: null), evitando vincoli sulla Root Directory.
// trailingSlash garantisce URL "puliti" via index.html per ogni route.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  eslint: {
    // La qualita' del codice e' garantita da `tsc --noEmit`; il lint non blocca il build.
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
