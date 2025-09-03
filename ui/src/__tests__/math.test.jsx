import { describe, it, expect } from 'vitest';

describe('math', () => {
  it('performs basic arithmetic', () => {
    expect(1 + 1).toBe(2);
    expect(Math.sqrt(4)).toBe(2);
  });
});
