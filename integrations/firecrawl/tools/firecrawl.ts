import { z } from "zod";
import fs from "fs";
import path from "path";

const USER_AGENT = "NaestroBot/1.0";
const CONTACT_EMAIL = "contact@naestro.ai";

interface DomainLimit {
  qps: number;
  burst: number;
}

const policy = {
  allow: ["example.com"],
  deny: ["bad.com"],
  qpsDefault: 1,
  burst: 2,
  perDomain: {
    "example.com": { qps: 5, burst: 10 },
  } as Record<string, DomainLimit>,
};

const domainStates = new Map<
  string,
  { tokens: number; last: number; queue: Promise<any> }
>();
const robotsCache = new Map<string, { disallow: string[] }>();

interface CrawlLedgerEntry {
  url: string;
  depth: number;
  status: number;
  bytes: number;
  runtime: number;
}

const ledgerPath = path.join(
  process.cwd(),
  "integrations",
  "firecrawl",
  "crawl-ledger.jsonl"
);

function recordLedger(entry: CrawlLedgerEntry) {
  try {
    fs.appendFileSync(ledgerPath, JSON.stringify(entry) + "\n");
  } catch {
    /* ignore ledger write errors */
  }
}

function getLimit(domain: string): DomainLimit {
  return policy.perDomain[domain] ?? {
    qps: policy.qpsDefault,
    burst: policy.burst,
  };
}

function enforceAllowDeny(domain: string) {
  if (policy.deny.includes(domain)) {
    throw new Error(`Domain denied by policy: ${domain}`);
  }
  if (policy.allow.length && !policy.allow.includes(domain)) {
    throw new Error(`Domain not allowed by policy: ${domain}`);
  }
}

async function ensureRobotsAllowed(url: URL) {
  let robots = robotsCache.get(url.origin);
  if (!robots) {
    robots = await fetchRobots(url);
    robotsCache.set(url.origin, robots);
  }
  for (const rule of robots.disallow) {
    if (rule && url.pathname.startsWith(rule)) {
      throw new Error(`Blocked by robots.txt: ${url.href}`);
    }
  }
}

async function fetchRobots(url: URL): Promise<{ disallow: string[] }> {
  try {
    const res = await fetch(`${url.origin}/robots.txt`, {
      headers: {
        "User-Agent": USER_AGENT,
        From: CONTACT_EMAIL,
      },
    });
    if (!res.ok) return { disallow: [] };
    const text = await res.text();
    const lines = text.split(/\r?\n/);
    const disallow: string[] = [];
    let applicable = false;
    for (const line of lines) {
      const ua = line.match(/^\s*User-agent:\s*(.*)/i);
      if (ua) {
        const agent = ua[1].trim();
        applicable = agent === "*" || agent.toLowerCase() === USER_AGENT.toLowerCase();
        continue;
      }
      if (!applicable) continue;
      const dis = line.match(/^\s*Disallow:\s*(.*)/i);
      if (dis) {
        disallow.push(dis[1].trim());
      }
    }
    return { disallow };
  } catch {
    return { disallow: [] };
  }
}

function getState(domain: string) {
  let state = domainStates.get(domain);
  if (!state) {
    const limit = getLimit(domain);
    state = { tokens: limit.burst, last: Date.now(), queue: Promise.resolve() };
    domainStates.set(domain, state);
  }
  return state;
}

function scheduleDomain<T>(domain: string, fn: () => Promise<T>): Promise<T> {
  const state = getState(domain);
  const run = async () => {
    const limit = getLimit(domain);
    const now = Date.now();
    const elapsed = (now - state!.last) / 1000;
    state!.tokens = Math.min(limit.burst, state!.tokens + elapsed * limit.qps);
    state!.last = now;
    if (state!.tokens < 1) {
      const waitMs = ((1 - state!.tokens) / limit.qps) * 1000;
      await new Promise((r) => setTimeout(r, waitMs));
      return scheduleDomain(domain, fn);
    }
    state!.tokens -= 1;
    return fn();
  };
  state.queue = state.queue.then(run);
  return state.queue as Promise<T>;
}

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
  const target = new URL(body.url);
  const domain = target.hostname;

  enforceAllowDeny(domain);
  await ensureRobotsAllowed(target);

  return scheduleDomain(domain, async () => {
    const start = Date.now();
    const res = await fetch("https://api.firecrawl.dev/v1/crawl", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        From: CONTACT_EMAIL,
        ...(apiKey ? { "X-API-Key": apiKey } : {}),
      },
      body: JSON.stringify(body),
    });

    const runtime = Date.now() - start;
    const text = await res.text();
    const bytes = Buffer.byteLength(text);
    const depth = (body as any).depth ?? 0;
    recordLedger({
      url: body.url,
      depth,
      status: res.status,
      bytes,
      runtime,
    });

    if (!res.ok) {
      throw new Error(`Firecrawl request failed: ${res.status} ${text}`);
    }

    return JSON.parse(text);
  });
}
