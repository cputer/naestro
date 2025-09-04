import { render, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MetricsChart from '../MetricsChart.jsx';

const createMetricsStream = () => {
  let emit;
  let reject;
  const getMetrics = vi.fn((e) => {
    emit = e;
    return new Promise((_, r) => {
      reject = r;
    });
  });
  return {
    getMetrics,
    emit: (m) => emit(m),
    error: () => reject(new Error('fail')),
  };
};

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
  it('renders empty response', async () => {
    const stream = createMetricsStream();
    const { getByRole } = render(
      <MetricsChart getMetrics={stream.getMetrics} />
    );
    act(() => {
      stream.emit([]);
    });
    await waitFor(() => {
      expect(getByRole('chart').getAttribute('data-points')).toBe('0');
    });
  });

  it('renders metrics with axes and legend', async () => {
    const stream = createMetricsStream();
    const metrics = [{ time: 1, latency: 2, throughput: 3 }];
    const { getByRole, container } = render(
      <MetricsChart getMetrics={stream.getMetrics} />
    );
    act(() => {
      stream.emit(metrics);
    });
    await waitFor(() => {
      expect(getByRole('chart').getAttribute('data-points')).toBe('1');
    });
    expect(getByRole('x-axis')).toBeInTheDocument();
    expect(getByRole('legend')).toBeInTheDocument();
    expect(container).toMatchSnapshot();
  });

  it('handles a single metric object', async () => {
    const stream = createMetricsStream();
    const { getByRole } = render(
      <MetricsChart getMetrics={stream.getMetrics} />
    );
    act(() => {
      stream.emit({ time: 1, latency: 2, throughput: 3 });
    });
    await waitFor(() => {
      expect(getByRole('chart').getAttribute('data-points')).toBe('1');
    });
  });

  it('uses cleanup returned from getMetrics', async () => {
    const cleanup = vi.fn();
    const getMetrics = vi.fn(() => cleanup);
    const { unmount } = render(<MetricsChart getMetrics={getMetrics} />);
    await waitFor(() => expect(getMetrics).toHaveBeenCalled());
    unmount();
    expect(cleanup).toHaveBeenCalled();
  });

  it('handles errors', async () => {
    const stream = createMetricsStream();
    const { getByRole } = render(
      <MetricsChart getMetrics={stream.getMetrics} />
    );
    act(() => {
      stream.error();
    });
    await waitFor(() => {
      expect(getByRole('alert')).toBeInTheDocument();
    });
  });
});

