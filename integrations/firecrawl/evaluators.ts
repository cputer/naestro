import crypto from "crypto";

export function evaluateCoverage(sitemapUrls: string[], fetchedUrls: string[]) {
  const fetchedSet = new Set(fetchedUrls);
  const missing = sitemapUrls.filter((u) => !fetchedSet.has(u));
  const coverage = sitemapUrls.length
    ? (sitemapUrls.length - missing.length) / sitemapUrls.length
    : 0;
  return { coverage, missing };
}

function detectLanguage(text: string): string {
  if (new RegExp("[\\u4e00-\\u9fff]").test(text)) return "zh";
  if (new RegExp("[\\u0400-\\u04FF]").test(text)) return "ru";
  return "en";
}

export interface PageData {
  url: string;
  content: string;
  canonicalUrl?: string;
}

export function evaluateContentQuality(pages: PageData[]) {
  const seen = new Map<string, string>();
  const duplicates: string[] = [];
  const languages: Record<string, number> = {};

  for (const p of pages) {
    const hash = crypto.createHash("md5").update(p.content).digest("hex");
    if (seen.has(hash)) {
      duplicates.push(p.url);
    } else {
      seen.set(hash, p.url);
    }
    const lang = detectLanguage(p.content);
    languages[lang] = (languages[lang] || 0) + 1;
  }

  return { duplicates, languages };
}

export function runSafetyChecks(pages: PageData[]) {
  const piiRegex = /\b\d{3}-\d{2}-\d{4}\b|\b\d{16}\b|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i;
  const secretRegex = /(api[_-]?key|secret|password)[\s:=]+[A-Za-z0-9\-_=+/]{8,}/i;
  const pii: string[] = [];
  const secrets: string[] = [];
  const nonCanonical: string[] = [];

  for (const p of pages) {
    if (piiRegex.test(p.content)) pii.push(p.url);
    if (secretRegex.test(p.content)) secrets.push(p.url);
    if (p.canonicalUrl && p.canonicalUrl !== p.url) nonCanonical.push(p.url);
  }

  return { pii, secrets, nonCanonical };
}

