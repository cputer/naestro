import {
  renderWithProviders,
  renderHookWithProviders,
  screen,
  waitFor,
} from './test-utils';
import { useEffect, useState } from 'react';
import { describe, it, expect } from 'vitest';

function AsyncComponent() {
  const [text, setText] = useState('loading');
  useEffect(() => {
    const timer = setTimeout(() => {
      setText('loaded');
    }, 0);
    return () => clearTimeout(timer);
  }, []);
  return <div>{text}</div>;
}

describe('renderWithProviders', () => {
  it('renders and waits for async content', async () => {
    renderWithProviders(<AsyncComponent />);
    await waitFor(() => {
      expect(screen.getByText('loaded')).toBeInTheDocument();
    });
  });
});

describe('renderHookWithProviders', () => {
  function useTestHook(initialValue: string) {
    const [value] = useState(initialValue);
    return value;
  }

  it('passes initial props to the hook', () => {
    const { result } = renderHookWithProviders(useTestHook, {
      initialProps: 'hello',
    });

    expect(result.current).toBe('hello');
  });
});
