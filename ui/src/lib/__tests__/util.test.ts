import { describe, it, expect } from 'vitest';

function normalizeLatency(ms: number): number {
  return ms / 1000;
}

describe('normalizeLatency', () => {
  it('converts milliseconds to seconds', () => {
    expect(normalizeLatency(500)).toBe(0.5);
    expect(normalizeLatency(1230)).toBeCloseTo(1.23);
  });

  it('handles zero latency', () => {
    expect(normalizeLatency(0)).toBe(0);
  });
});
