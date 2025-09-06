export interface Chunk {
  heading: string | null;
  text: string;
}

/**
 * Splits a markdown string into semantic chunks. Headings break sections and
 * long sections are further split by length.
 */
export function chunkWithHeadings(
  input: string,
  maxLen = 1000
): Chunk[] {
  const lines = input.split(/\r?\n/);
  let current: string | null = null;
  let buf: string[] = [];
  const chunks: Chunk[] = [];

  const push = () => {
    if (!buf.length) return;
    chunks.push({ heading: current, text: buf.join("\n").trim() });
    buf = [];
  };

  for (const line of lines) {
    const m = line.match(/^(#{1,6})\s+(.*)/);
    if (m) {
      push();
      current = m[2].trim();
      continue;
    }
    if (buf.join("\n").length + line.length > maxLen) {
      push();
    }
    buf.push(line);
  }
  push();
  return chunks.filter((c) => c.text);
}
