import { describe, it, expect, vi } from 'vitest';
import React from 'react';
import { render, screen } from '@testing-library/react';
import CodeEditor from '../CodeEditor.jsx';

vi.mock('@monaco-editor/react', () => ({
  Editor: () => <div>mock editor</div>,
  DiffEditor: () => <div>mock diff editor</div>,
}));

describe('CodeEditor', () => {
  it('renders with defaults', () => {
    render(<CodeEditor language="plaintext" />);
    expect(screen.getByText('mock editor')).toBeTruthy();
  });
});
