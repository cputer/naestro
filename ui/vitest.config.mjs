import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    coverage: {
      all: true,
      include: ['src/**/*.{js,jsx,ts,tsx}'],
      exclude: ['src/**/__tests__/**', 'src/setupTests.ts', 'src/main.jsx'],
      perFile: true,
      reporter: ['text', 'lcov', 'html'],
      lines: 100,
      statements: 100,
      branches: 100,
      functions: 100,
    },
  },
});

