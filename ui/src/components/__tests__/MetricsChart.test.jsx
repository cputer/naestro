import { render, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import MetricsChart from '../MetricsChart.jsx';

const listeners = {};

vi.mock('socket.io-client', () => ({
  default: vi.fn(() => ({
    on: vi.fn((event, cb) => {
      listeners[event] = cb;
    }),
    close: vi.fn(),
  })),
}));

vi.mock('recharts', () => ({
  ResponsiveContainer: ({ children }) => <div data-testid="container">{children}</div>,
  LineChart: ({ data, children }) => (
    <div data-testid="chart" data-points={data.length}>
      {children}
    </div>
  ),
  CartesianGrid: () => null,
  XAxis: () => null,
  YAxis: () => null,
  Tooltip: () => null,
  Legend: () => null,
  Line: ({ dataKey }) => <div data-testid={`line-${dataKey}`} />,
}));

describe('MetricsChart', () => {
  beforeEach(() => {
    for (const key in listeners) delete listeners[key];
  });

  it('renders without data', () => {
    const { getByTestId } = render(<MetricsChart />);
    expect(getByTestId('chart').getAttribute('data-points')).toBe('0');
  });

  it('renders with series data', () => {
    const { getByTestId } = render(<MetricsChart />);
    act(() => {
      listeners.metrics({ time: 1, latency: 2, throughput: 3 });
    });
    expect(getByTestId('chart').getAttribute('data-points')).toBe('1');
    expect(getByTestId('line-latency')).toBeInTheDocument();
    expect(getByTestId('line-throughput')).toBeInTheDocument();
  });
});
