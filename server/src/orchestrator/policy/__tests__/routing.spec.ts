import { describe, it, expect } from 'vitest';
import { chooseRoute } from '../routing';

describe('chooseRoute', () => {
  it('uses local route when token count is below threshold and local route available', () => {
    expect(chooseRoute({ tokens: 1500 })).toBe('local');
  });

  it('falls back to cloud when token count exceeds threshold', () => {
    expect(chooseRoute({ tokens: 250000 })).toBe('cloud');
  });

  it('falls back to cloud when local route is unavailable', () => {
    expect(chooseRoute({ tokens: 1500, localAvailable: false })).toBe('cloud');
  });
});
