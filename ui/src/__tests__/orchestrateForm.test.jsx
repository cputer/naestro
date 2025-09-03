import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import React, { useState } from 'react';
import { server } from '../mocks/server.js';
import { http, HttpResponse } from 'msw';
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

beforeEach(() => {
  server.use(
    http.post('http://localhost/api/orchestrate', () =>
      HttpResponse.json({ id: 'mocked-id' })
    )
  );
});

function OrchestrateForm() {
  const [id, setId] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    const resp = await fetch('http://localhost/api/orchestrate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task: 'demo' })
    });
    const data = await resp.json();
    setId(data.id);
  };

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit">Run</button>
      {id && <div role="status">{id}</div>}
    </form>
  );
}

describe('Orchestrate form', () => {
  it('submits and displays returned id', async () => {
    render(<OrchestrateForm />);
    fireEvent.click(screen.getByRole('button', { name: /run/i }));
    const status = await screen.findByRole('status');
    expect(status).toHaveTextContent('mocked-id');
  });
});

