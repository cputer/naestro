import { describe, it, expect } from 'vitest';
import { estimateTokens } from '../token';

describe('estimateTokens', () => {
  it('estimates tokens for a single string', () => {
    expect(estimateTokens('hello world')).toBe(2);
  });

  it('handles arrays of strings', () => {
    expect(estimateTokens(['hello world', 'how are you'])).toBe(5);
  });

  it('returns 0 for empty input', () => {
    expect(estimateTokens('')).toBe(0);
    expect(estimateTokens([])).toBe(0);
  });
});
