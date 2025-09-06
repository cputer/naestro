import { z } from "zod";

// Schema for Firecrawl crawl options. Additional fields are passed through to the API.
export const FirecrawlSchema = z
  .object({
    url: z.string().url(),
    apiKey: z.string().optional(),
  })
  .passthrough();

export type FirecrawlOptions = z.infer<typeof FirecrawlSchema>;

/**
 * Calls the Firecrawl crawl API.
 * @param options Parameters for the crawl request.
 * @returns JSON response from the Firecrawl API.
 */
export async function firecrawl(options: FirecrawlOptions) {
  const { apiKey, ...body } = FirecrawlSchema.parse(options);

  const res = await fetch("https://api.firecrawl.dev/v1/crawl", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(apiKey ? { "X-API-Key": apiKey } : {}),
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Firecrawl request failed: ${res.status} ${text}`);
  }

  return res.json();
}
