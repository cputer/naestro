import { describe, it, expect } from 'vitest';

describe('ui smoke', () => {
  it('jsdom present', () => {
    expect(typeof document).toBe('object');
  });
});
