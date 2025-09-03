import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/models', () => {
    return HttpResponse.json({ models: [] });
  }),
  http.get('/api/health', () => {
    return HttpResponse.json({ status: 'ok' });
  }),
  http.post('/api/orchestrate', () => {
    return HttpResponse.json({ id: 'mocked-id' });
  }),
];
