import { describe, it, expect } from 'vitest';

describe('smoke', () => {
  it('jsdom is available', () => {
    expect(typeof window).toBe('object');
    expect(typeof document).toBe('object');
  });
});
