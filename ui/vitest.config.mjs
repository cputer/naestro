import { defineConfig, configDefaults, coverageConfigDefaults } from 'vitest/config';
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    css: true,
    exclude: [...configDefaults.exclude, 'src/main.jsx'],
    coverage: {
      provider: 'v8',
      all: true,
      include: ['src/**/*.{js,jsx,ts,tsx}'],
      exclude: [...coverageConfigDefaults.exclude, 'src/main.jsx', 'src/**/__tests__/**', 'src/mocks/**'],
      reporter: ['text', 'html', 'lcov'],
      reportsDirectory: './coverage',
      lines: 100,
      functions: 100,
      statements: 100,
      branches: 100,
    },
  },
});
