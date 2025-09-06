# Firecrawl Integration

[← Back to INTEGRATIONS](../INTEGRATIONS.md)

## Usage
The Firecrawl crawler is exposed as a tool via the registry. Register `firecrawl:crawl` and supply a target URL when invoking it. The tool definition lives in [`registry/tools.json`](../../registry/tools.json).

Example invocation:

```json
{
  "tool": "firecrawl:crawl",
  "args": { "url": "https://example.com" }
}
```

Studio provides a Firecrawl panel for interactive testing and exporting n8n flows; see [`studio/panels/FirecrawlPanel.tsx`](../../studio/panels/FirecrawlPanel.tsx).

## Capabilities
- Validates crawl requests and normalizes mixed-case URLs
- Extracts page headings and stores embeddings for each document
- Computes sitemap coverage ratios to report uncrawled pages
- Maps domain and HTTP errors to structured responses

## Policy
Crawling respects an allow/deny list and robots.txt rules:

- Allowed domains: `example.com`
- Denied domains: `bad.com`
- Default rate limit: 1 QPS with burst 2

These defaults can be adjusted in the source.
