import { chunkWithHeadings, Chunk } from "./chunker";

interface FirecrawlItem {
  id?: string;
  url?: string;
  content?: string;
  markdown?: string;
  title?: string;
  [key: string]: any;
}

interface Doc {
  id: string;
  text: string;
  meta: Record<string, any>;
}

interface DocWithEmbedding extends Doc {
  embedding: number[];
}

function detectLanguage(text: string): string {
  if (new RegExp("[\\u4e00-\\u9fff]").test(text)) return "zh";
  if (new RegExp("[\\u0400-\\u04FF]").test(text)) return "ru";
  return "en";
}

function detectPageType(text: string): string {
  if (/\|.*\|/.test(text)) return "table";
  if (/^\s*[-*]\s/m.test(text)) return "list";
  return "text";
}

function normalizeItem(item: FirecrawlItem): Doc {
  const text = item.markdown ?? item.content ?? "";
  const language = detectLanguage(text);
  const pageType = detectPageType(text);
  return {
    id: item.id || item.uuid || item.url || Math.random().toString(36).slice(2),
    text,
    meta: {
      source: "firecrawl",
      url: item.url,
      title: item.title,
      language,
      pageType,
    },
  };
}

async function embedBatch(texts: string[]): Promise<number[][]> {
  return texts.map((t) => Array.from(Buffer.from(t)).map((b) => b / 255));
}

async function upsertDocs(_docs: DocWithEmbedding[]): Promise<void> {
  return;
}

export async function ingestFirecrawl(items: FirecrawlItem[]) {
  const docs = items.map(normalizeItem);

  const chunks: Doc[] = [];
  for (const doc of docs) {
    const parts = chunkWithHeadings(doc.text);
    parts.forEach((p: Chunk, idx: number) => {
      chunks.push({
        id: `${doc.id}:${idx}`,
        text: p.text,
        meta: { ...doc.meta, heading: p.heading },
      });
    });
  }

  const embeddings = await embedBatch(chunks.map((c) => c.text));
  const withEmbeddings: DocWithEmbedding[] = chunks.map((c, i) => ({
    ...c,
    embedding: embeddings[i],
  }));
  await upsertDocs(withEmbeddings);

  return withEmbeddings;
}
