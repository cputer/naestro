import type { Request, Response } from "express";
export function healthHandler(_req: Request, res: Response) {
  const core = process.env.NAESTRO_VERSION || "1.4.0";
  const studio = process.env.NAESTRO_STUDIO_VERSION || "0.9.2";
  const providers = process.env.NAESTRO_PROVIDERS_SCHEMA || "0.6";
  const git = process.env.GIT_SHA || process.env.VERCEL_GIT_COMMIT_SHA || "unknown";
  res.setHeader("X-Naestro-Version", core);
  res.json({ core, studio, providers_schema: providers, git_sha: git, ok: true });
}
