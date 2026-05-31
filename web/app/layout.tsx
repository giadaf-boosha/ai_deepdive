import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./globals.css";
import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: {
    default: "AI Deep Dive",
    template: "%s — AI Deep Dive",
  },
  description:
    "La mia raccolta quotidiana di segnali AI, in italiano. Digest curati, knowledge base tecnica e radar dei modelli AI.",
  metadataBase: new URL("https://ai-deepdive.vercel.app"),
  openGraph: {
    title: "AI Deep Dive",
    description: "La mia raccolta quotidiana di segnali AI, in italiano.",
    type: "website",
    locale: "it_IT",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="it" className={`${GeistSans.variable} ${GeistMono.variable}`}>
      <body className="flex min-h-screen flex-col font-sans">
        <Nav />
        <main className="flex-1 pb-20 pt-8">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
