import type { ReactElement } from 'react';
import { render, screen, waitFor } from '@testing-library/react';

export function renderWithProviders(ui: ReactElement) {
  // Extend here with providers if needed (Router, QueryClient, etc.)
  return render(ui);
}

export { screen, waitFor };

