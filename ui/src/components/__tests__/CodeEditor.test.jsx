import { describe, it, expect, vi } from 'vitest';
import React from 'react';
import { render } from '@testing-library/react';
import CodeEditor from '../CodeEditor.jsx';

vi.mock('@monaco-editor/react', () => ({
  Editor: () => <div>mock editor</div>,
  DiffEditor: () => <div>mock diff editor</div>,
}));

describe('CodeEditor', () => {
  it('renders with defaults', () => {
    const { getByText } = render(<CodeEditor language="plaintext" />);
    expect(getByText('mock editor')).toBeTruthy();
  });
});
