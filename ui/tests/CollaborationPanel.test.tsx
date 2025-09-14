import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import React from 'react';
import CollaborationPanel, { CollaborationPrefs } from '../components/CollaborationPanel';

describe('CollaborationPanel', () => {
  it('loads preferences on mount', async () => {
    const loadPrefs = vi.fn().mockResolvedValue({ mode: 'solo', depth: 2 });
    render(<CollaborationPanel loadPrefs={loadPrefs} />);
    expect(await screen.findByDisplayValue('solo')).toBeInTheDocument();
    expect(loadPrefs).toHaveBeenCalled();
  });

  it('saves updated preferences', async () => {
    const loadPrefs = vi.fn().mockResolvedValue({ mode: 'solo', auto: false });
    const savePrefs = vi.fn().mockResolvedValue({});
    render(
      <CollaborationPanel loadPrefs={loadPrefs} savePrefs={savePrefs} />
    );
    await screen.findByDisplayValue('solo');
    fireEvent.change(screen.getByLabelText(/Mode/i), {
      target: { value: 'consult' },
    });
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    expect(savePrefs).toHaveBeenCalledWith(
      expect.objectContaining({ mode: 'consult' })
    );
  });
});

