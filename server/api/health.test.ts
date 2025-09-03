import type { Request, Response } from 'express';
import { describe, expect, it, vi } from 'vitest';
import { healthHandler } from './health';

describe('healthHandler', () => {
  it('responds with ok', () => {
    const req = {} as Request;
    const setHeader = vi.fn();
    const json = vi.fn();

    const res = { setHeader, json } as unknown as Response;

    healthHandler(req, res);

    expect(setHeader).toHaveBeenCalledWith('X-Naestro-Version', expect.any(String));
    expect(json).toHaveBeenCalledWith(expect.objectContaining({ ok: true }));
  });
});
