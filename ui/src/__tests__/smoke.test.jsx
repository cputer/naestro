import { describe, it, expect } from 'vitest';

describe('ui smoke', () => {
  it('runs vitest in jsdom', () => {
    expect(typeof document).toBe('object');
  });
});
