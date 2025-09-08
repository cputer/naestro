import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import * as FirecrawlTool from '../tools/firecrawl';
import { ingestFirecrawl } from '../ingest';
import { evaluateCoverage } from '../evaluators';

const { FirecrawlSchema, firecrawl } = FirecrawlTool;
const originalFetch = global.fetch;
const fixturePath = path.join(__dirname, 'fixtures', 'example-site.json');

// helper to load fixture items
function loadExampleItems() {
  const data = fs.readFileSync(fixturePath, 'utf-8');
  return JSON.parse(data);
}

describe('Firecrawl schema validation', () => {
  it('accepts valid options', () => {
    const opts = { url: 'https://example.com' };
    expect(FirecrawlSchema.parse(opts)).toMatchObject(opts);
  });

  it('rejects invalid url', () => {
    expect(() => FirecrawlSchema.parse({ url: 'not-a-url' } as any)).toThrow();
  });
});

describe('Firecrawl URL normalization', () => {
  beforeEach(() => {
    vi.spyOn(fs, 'appendFileSync').mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
    global.fetch = originalFetch;
  });

  it('allows mixed-case domains via normalization', async () => {
    const fetchMock = vi
      .fn()
      // robots.txt request
      .mockResolvedValueOnce({ ok: true, text: async () => '' })
      // crawl API request
      .mockResolvedValueOnce({ ok: true, text: async () => '{"items":[]}' });

    // @ts-ignore
    global.fetch = fetchMock;

    await firecrawl({ url: 'HTTPS://EXAMPLE.COM' });

    expect(fetchMock).toHaveBeenCalledWith(
      'https://example.com/robots.txt',
      expect.any(Object)
    );
    expect(fetchMock).toHaveBeenCalledWith(
      'https://api.firecrawl.dev/v1/crawl',
      expect.objectContaining({ method: 'POST' })
    );
  });
});

describe('Firecrawl error mapping', () => {
  beforeEach(() => {
    vi.spyOn(fs, 'appendFileSync').mockImplementation(() => {});
    (FirecrawlTool as any).robotsCache?.clear?.();
    (FirecrawlTool as any).domainStates?.clear?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    global.fetch = originalFetch;
  });

  it('rejects denied domains', async () => {
    await expect(firecrawl({ url: 'https://bad.com' })).rejects.toThrow(
      /Domain denied by policy: bad.com/
    );
  });

  it('rejects domains outside allow list', async () => {
    await expect(firecrawl({ url: 'https://unknown.com' })).rejects.toThrow(
      /Domain not allowed by policy: unknown.com/
    );
  });

  it('maps HTTP errors to thrown errors', async () => {
    const fetchMock = vi.fn((url: string) =>
      Promise.resolve(
        url.endsWith('/robots.txt')
          ? { ok: true, text: async () => '' }
          : { ok: false, status: 500, text: async () => 'boom' }
      )
    );

    // @ts-ignore
    global.fetch = fetchMock;

    await expect(firecrawl({ url: 'https://example.com' })).rejects.toThrow(
      /Firecrawl request failed: 500 boom/
    );
  });
});

describe('Firecrawl robots.txt handling', () => {
  let firecrawl: any;
  beforeEach(async () => {
    vi.spyOn(fs, 'appendFileSync').mockImplementation(() => {});
    await vi.resetModules();
    const mod: any = await import('../tools/firecrawl');
    firecrawl = mod.firecrawl;
    mod.robotsCache?.clear?.();
    mod.domainStates?.clear?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    global.fetch = originalFetch;
  });

  it('rejects URLs blocked by robots.txt', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        text: async () => 'User-agent: *\nDisallow: /private',
      });

    // @ts-ignore
    global.fetch = fetchMock;

    await expect(
      firecrawl({ url: 'https://example.com/private/page' })
    ).rejects.toThrow(/Blocked by robots.txt/);

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock).toHaveBeenCalledWith(
      'https://example.com/robots.txt',
      expect.any(Object)
    );
  });
});

describe('Firecrawl ledger logging', () => {
  let firecrawl: any;
  beforeEach(async () => {
    await vi.resetModules();
    const mod: any = await import('../tools/firecrawl');
    firecrawl = mod.firecrawl;
    mod.robotsCache?.clear?.();
    mod.domainStates?.clear?.();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    global.fetch = originalFetch;
  });

  it('records crawl details to the ledger', async () => {
    const appendSpy = vi
      .spyOn(fs, 'appendFileSync')
      .mockImplementation(() => {});

    const fetchMock = vi
      .fn()
      // robots.txt request
      .mockResolvedValueOnce({ ok: true, text: async () => '' })
      // crawl API request
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        text: async () => '{"items":[]}',
      });

    // @ts-ignore
    global.fetch = fetchMock;

    await firecrawl({ url: 'https://example.com/foo', depth: 3 });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(appendSpy).toHaveBeenCalledTimes(1);
    const [filePath, content] = appendSpy.mock.calls[0];
    expect(filePath).toMatch(/crawl-ledger\.jsonl$/);
    const entry = JSON.parse(String(content).trim());
    expect(entry).toMatchObject({
      url: 'https://example.com/foo',
      depth: 3,
      status: 200,
    });
    expect(entry.bytes).toBeGreaterThan(0);
    expect(entry.runtime).toBeGreaterThanOrEqual(0);
  });
});

describe('Firecrawl end-to-end ingest', () => {
  it('parses headings, stores embeddings, and computes coverage', async () => {
    const items = loadExampleItems();
    const docs = await ingestFirecrawl(items);

    // headings parsed
    const headings = docs.map((d) => d.meta.heading);
    expect(headings).toContain('Welcome');
    expect(headings).toContain('Section');
    expect(headings).toContain('About');

    // embeddings stored
    for (const d of docs) {
      expect(Array.isArray(d.embedding)).toBe(true);
      expect(d.embedding.length).toBeGreaterThan(0);
    }

    // coverage ratio
    const sitemap = [
      'https://example.com',
      'https://example.com/about',
      'https://example.com/missing'
    ];
    const { coverage, missing } = evaluateCoverage(
      sitemap,
      items.map((i: any) => i.url)
    );
    expect(coverage).toBeCloseTo(2 / 3);
    expect(missing).toEqual(['https://example.com/missing']);
  });
});
