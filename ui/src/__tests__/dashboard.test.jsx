import { vi, describe, it, expect } from 'vitest';
vi.mock('socket.io-client', () => ({
  default: vi.fn(() => ({ on: vi.fn(), close: vi.fn() }))
}));

import { server } from '../mocks/server.js';
import { http, HttpResponse } from 'msw';
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

beforeEach(() => {
  server.use(
    http.get('http://localhost/api/models', () =>
      HttpResponse.json({ models: [] })
    )
  );
});

import { render, screen } from '@testing-library/react';
import App from '../App.jsx';

class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
global.ResizeObserver = ResizeObserver;

// Dashboard rendering and API fetch behavior

describe('Dashboard', () => {
  it('renders dashboard heading', () => {
    render(<App />);
    expect(
      screen.getByRole('heading', { name: /naestro dashboard/i })
    ).toBeInTheDocument();
  });

  it('fetches data from the models API', async () => {
    render(<App />);
    const res = await fetch('http://localhost/api/models');
    const data = await res.json();
    expect(data).toEqual({ models: [] });
  });
});

