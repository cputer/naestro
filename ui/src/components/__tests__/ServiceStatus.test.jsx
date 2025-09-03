import { render, screen, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ServiceStatus from '../ServiceStatus.jsx';

const listeners = {};

vi.mock('socket.io-client', () => ({
  default: vi.fn(() => ({
    on: vi.fn((event, cb) => {
      listeners[event] = cb;
    }),
    close: vi.fn(),
  })),
}));

describe('ServiceStatus', () => {
  beforeEach(() => {
    for (const key in listeners) delete listeners[key];
  });

  it.each([
    ['ok', 'MuiChip-colorSuccess'],
    ['warn', 'MuiChip-colorWarning'],
    ['error', 'MuiChip-colorError'],
    ['unknown', 'MuiChip-colorDefault'],
  ])('renders %s status', (state, className) => {
    render(<ServiceStatus />);
    act(() => {
      listeners.status({ svc: state });
    });
    const chip = screen.getByText(`svc: ${state}`).closest('.MuiChip-root');
    expect(chip).toHaveClass(className);
  });

  it('falls back to default color for unrecognized status', () => {
    render(<ServiceStatus />);
    act(() => {
      listeners.status({ svc: 'offline' });
    });
    const chip = screen.getByText('svc: offline').closest('.MuiChip-root');
    expect(chip).toHaveClass('MuiChip-colorDefault');
  });

  it('mocks API endpoints', async () => {
    const health = await fetch('/api/health');
    expect(await health.json()).toEqual({ status: 'ok' });

    const models = await fetch('/api/models');
    expect(await models.json()).toEqual({ models: [] });

    const orchestrate = await fetch('/api/orchestrate', { method: 'POST' });
    expect(await orchestrate.json()).toEqual({ id: 'mocked-id' });
  });
});
