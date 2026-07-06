import Link from "next/link";
import type { ComponentPropsWithoutRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import { rewriteKbLinks, rewriteFondamentiLinks } from "@/lib/markdown";

function Anchor({ href, children, ...rest }: ComponentPropsWithoutRef<"a">) {
  if (!href) return <a {...rest}>{children}</a>;
  if (/^https?:\/\//.test(href)) {
    return (
      <a href={href} target="_blank" rel="noreferrer" {...rest}>
        {children}
      </a>
    );
  }
  return (
    <Link href={href} {...rest}>
      {children}
    </Link>
  );
}

export function MarkdownContent({
  content,
  rewriteKb = false,
  rewriteFondamenti = false,
}: {
  content: string;
  rewriteKb?: boolean;
  rewriteFondamenti?: boolean;
}) {
  const source = rewriteKb
    ? rewriteKbLinks(content)
    : rewriteFondamenti
      ? rewriteFondamentiLinks(content)
      : content;
  return (
    <div className="prose-deepdive">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw, rehypeSlug]}
        components={{ a: Anchor }}
      >
        {source}
      </ReactMarkdown>
    </div>
  );
}
