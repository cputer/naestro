import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { firecrawl } from '../../integrations/firecrawl/tools/firecrawl';
import { ingestFirecrawl } from '../../integrations/firecrawl/ingest';
import { evaluateCoverage } from '../../integrations/firecrawl/evaluators';

const fixturePath = path.join(
  __dirname,
  '../../integrations/firecrawl/__tests__/fixtures/example-site.json'
);
function loadExampleItems() {
  return JSON.parse(fs.readFileSync(fixturePath, 'utf-8'));
}

describe('Firecrawl e2e ingest flow', () => {
  const originalFetch = global.fetch;
  const ledgerPath = path.join(
    process.cwd(),
    'integrations',
    'firecrawl',
    'crawl-ledger.jsonl'
  );
  let server: http.Server;
  let port: number;

  beforeAll(async () => {
    const items = loadExampleItems();
    server = http.createServer((req, res) => {
      if (req.url === '/robots.txt') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('');
      } else if (req.url === '/v1/crawl' && req.method === 'POST') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ items }));
      } else {
        res.writeHead(404);
        res.end();
      }
    });
    await new Promise<void>((resolve) => {
      server.listen(0, () => {
        const addr = server.address() as any;
        port = addr.port;
        resolve();
      });
    });

    // redirect fetches to our mock server
    // @ts-ignore
    global.fetch = (url: any, init?: any) => {
      const u = new URL(url);
      if (u.hostname === 'api.firecrawl.dev') {
        return originalFetch(`http://localhost:${port}/v1/crawl`, init);
      }
      if (u.hostname === 'example.com') {
        return originalFetch(`http://localhost:${port}${u.pathname}`, init);
      }
      return originalFetch(url, init);
    };

    if (fs.existsSync(ledgerPath)) fs.unlinkSync(ledgerPath);
  });

  afterAll(() => {
    global.fetch = originalFetch;
    server.close();
    if (fs.existsSync(ledgerPath)) fs.unlinkSync(ledgerPath);
  });

  it('ingests pages and records ledger with coverage metrics', async () => {
    const result = await firecrawl({ url: 'https://example.com', depth: 1 });
    const docs = await ingestFirecrawl(result.items);
    expect(docs.length).toBeGreaterThan(0);

    // ledger persisted
    const raw = fs.readFileSync(ledgerPath, 'utf-8').trim();
    const entry = JSON.parse(raw.split('\n')[0]);
    expect(entry).toMatchObject({
      url: 'https://example.com',
      depth: 1,
      status: 200,
    });
    expect(entry.bytes).toBeGreaterThan(0);

    // coverage metrics
    const sitemap = [
      'https://example.com',
      'https://example.com/about',
      'https://example.com/missing',
    ];
    const { coverage, missing } = evaluateCoverage(
      sitemap,
      result.items.map((i: any) => i.url)
    );
    expect(coverage).toBeCloseTo(2 / 3);
    expect(missing).toEqual(['https://example.com/missing']);
  });
});

