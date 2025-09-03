import type { Request, Response } from 'express';
import { describe, expect, it, vi } from 'vitest';
import { healthHandler } from './health';

describe('healthHandler', () => {
  it('responds with version headers and full status payload', () => {
    const req = {} as Request;
    const setHeader = vi.fn();
    const json = vi.fn();
    const res = { setHeader, json } as unknown as Response;

    const prev = {
      NAESTRO_VERSION: process.env.NAESTRO_VERSION,
      NAESTRO_STUDIO_VERSION: process.env.NAESTRO_STUDIO_VERSION,
      NAESTRO_PROVIDERS_SCHEMA: process.env.NAESTRO_PROVIDERS_SCHEMA,
      GIT_SHA: process.env.GIT_SHA,
    };

    process.env.NAESTRO_VERSION = '1.2.3';
    process.env.NAESTRO_STUDIO_VERSION = '4.5.6';
    process.env.NAESTRO_PROVIDERS_SCHEMA = '7.8.9';
    process.env.GIT_SHA = 'abcdefg';

    try {
      healthHandler(req, res);
    } finally {
      process.env.NAESTRO_VERSION = prev.NAESTRO_VERSION;
      process.env.NAESTRO_STUDIO_VERSION = prev.NAESTRO_STUDIO_VERSION;
      process.env.NAESTRO_PROVIDERS_SCHEMA = prev.NAESTRO_PROVIDERS_SCHEMA;
      process.env.GIT_SHA = prev.GIT_SHA;
    }

    expect(setHeader).toHaveBeenCalledWith('X-Naestro-Version', '1.2.3');
    expect(json).toHaveBeenCalledWith({
      core: '1.2.3',
      studio: '4.5.6',
      providers_schema: '7.8.9',
      git_sha: 'abcdefg',
      ok: true,
    });
  });
});
