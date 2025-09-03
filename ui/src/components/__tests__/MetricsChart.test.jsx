import { render, act, waitFor } from '@testing-library/react';
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
  ResponsiveContainer: ({ children }) => (
    <div data-testid="container">{children}</div>
  ),
  LineChart: ({ data, children }) => (
    <div role="chart" data-points={data.length}>
      {children}
    </div>
  ),
  CartesianGrid: () => <div role="grid" />,
  XAxis: () => <div role="x-axis" />,
  YAxis: () => <div role="y-axis" />,
  Tooltip: () => <div role="tooltip" />,
  Legend: () => <div role="legend" />,
  Line: ({ dataKey }) => <div role={`line-${dataKey}`} />,
}));

describe('MetricsChart', () => {
  beforeEach(() => {
    for (const key in listeners) delete listeners[key];
  });

  it('renders empty response', async () => {
    const getMetrics = vi.fn((emit) => emit([]));
    const { getByRole } = render(<MetricsChart getMetrics={getMetrics} />);

    await waitFor(() => {
      expect(getByRole('chart').getAttribute('data-points')).toBe('0');
    });
  });

  it('renders metrics with axes and legend', async () => {
    const metrics = [{ time: 1, latency: 2, throughput: 3 }];
    const getMetrics = vi.fn((emit) => emit(metrics));
    const { getByRole, container } = render(
      <MetricsChart getMetrics={getMetrics} />
    );

    await waitFor(() => {
      expect(getByRole('chart').getAttribute('data-points')).toBe('1');
    });

    expect(getByRole('x-axis')).toBeInTheDocument();
    expect(getByRole('legend')).toBeInTheDocument();
    expect(container).toMatchSnapshot();
  });

  it('handles socket errors', () => {
    const { getByRole } = render(<MetricsChart />);
    act(() => {
      listeners.connect_error(new Error('fail'));
    });
    expect(getByRole('alert')).toBeInTheDocument();
  });
});

