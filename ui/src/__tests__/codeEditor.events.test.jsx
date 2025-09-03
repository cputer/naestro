import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import CodeEditor from '../components/CodeEditor.jsx';

describe('CodeEditor change events', () => {
  it('updates displayed code when props change', () => {
    const { rerender } = render(
      <CodeEditor original="foo" modified="bar" />
    );

    expect(screen.getByText('foo')).toBeInTheDocument();
    expect(screen.getByText('bar')).toBeInTheDocument();

    rerender(<CodeEditor original="foo" modified="baz" />);
    expect(screen.queryByText('bar')).not.toBeInTheDocument();
    expect(screen.getByText('baz')).toBeInTheDocument();
  });
});

