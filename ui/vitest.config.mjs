import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    reporters: ['dot'],
    include: ['src/**/*.{test,spec}.{js,jsx}'],
    watch: false,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'text-summary', 'lcov'],
      reportsDirectory: 'coverage',
      all: true,
      include: ['src/**/*.{js,jsx,ts,tsx}'],
      exclude: [
        'src/**/*.generated.{js,jsx,ts,tsx}',
        'src/**/*.stories.{js,jsx,ts,tsx}',
        'src/**/*.{setup,setupTests}.{js,jsx,ts,tsx}'
      ],
      thresholds: {
        lines: 100,
        functions: 100,
        branches: 100,
        statements: 100
      }
    }
  }
});
