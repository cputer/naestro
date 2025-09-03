import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect, vi } from 'vitest';

vi.mock('socket.io-client', () => ({
  default: vi.fn(() => ({ on: vi.fn(), close: vi.fn() }))
}));

import ServiceStatus from '../components/ServiceStatus.jsx';

describe('LiveMonitor', () => {
  it('renders no services initially', () => {
    const { container } = render(<ServiceStatus />);
    expect(container.firstChild).toBeEmptyDOMElement();
  });
});

