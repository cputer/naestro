import { http, HttpResponse } from 'msw';

// Mock API handlers used by dashboard components.
// Add new endpoints here so tests remain deterministic.
export const handlers = [
  // Models listing for orchestrate flow
  http.get('/api/models', () => {
    return HttpResponse.json({ models: [] });
  }),

  // Health check endpoint
  http.get('/api/health', () => {
    return HttpResponse.json({ status: 'ok' });
  }),

  // Orchestrate action
  http.post('/api/orchestrate', () => {
    return HttpResponse.json({ id: 'mocked-id' });
  }),

  // ServiceStatus & LiveMonitor: service state snapshot
  http.get('/api/status', () => {
    return HttpResponse.json({ svc: 'ok' });
  }),

  // MetricsChart: initial metrics snapshot
  http.get('/api/metrics', () => {
    return HttpResponse.json({ time: 0, latency: 0, throughput: 0 });
  }),
];
