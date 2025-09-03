import { render } from '@testing-library/react';
import { beforeAll, describe, it, expect } from 'vitest';
import App from '../../App.jsx';

beforeAll(() => {
  globalThis.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

describe('App component', () => {
  it('renders non-empty output', () => {
    const { container } = render(<App />);
    expect(container.innerHTML).not.toBe('');
  });
});
