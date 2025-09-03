import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.js'],
    coverage: {
      include: ['src/**/*.{js,jsx,ts,tsx}'],
      exclude: ['src/main.jsx', 'src/**/__tests__/**', 'src/setup.js'],
      perFile: true,
      reporter: ['text', 'lcov', 'html'],
    },
  },
});

