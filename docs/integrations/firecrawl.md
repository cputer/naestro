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

## Customizing Crawler Policy
The crawler policy is defined in [`integrations/firecrawl/tools/firecrawl.ts`](../../integrations/firecrawl/tools/firecrawl.ts). Update this file to tailor crawling behavior:

- **`allow`** – array of domains explicitly permitted. Leave empty to allow any domain.
- **`deny`** – domains that should always be blocked.
- **`qpsDefault`** – default queries per second for domains without overrides.
- **`perDomain`** – object mapping domains to custom `{ qps, burst }` limits.

Example snippet:

```ts
const policy = {
  allow: ["example.com"],
  deny: ["bad.com"],
  qpsDefault: 1,
  burst: 2,
  perDomain: {
    "example.com": { qps: 5, burst: 10 },
  },
};
```

Adjust these values and rebuild to enforce project‑specific rules.

## Studio Panel
To run manual tests or export an n8n flow:

1. Start the Studio development server from the `ui` directory: `npm install` and `npm run dev`.
2. Open `studio/panels/FirecrawlPanel.tsx` and mount it within your Studio project.
3. Use the panel form to configure a crawl, run it, and click **Export n8n flow** to download a ready‑to‑use workflow.

## Policy
Crawling respects an allow/deny list and robots.txt rules:

- Allowed domains: `example.com`
- Denied domains: `bad.com`
- Default rate limit: 1 QPS with burst 2

These defaults can be adjusted in the source.
