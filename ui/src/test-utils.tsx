import React, { ReactElement, ReactNode } from 'react';
import {
  render,
  renderHook,
  RenderHookOptions,
  RenderHookResult,
  RenderOptions,
  RenderResult,
} from '@testing-library/react';

type WrapperProps = { children: ReactNode };

function TestProviders({ children }: WrapperProps) {
  // Extend here with providers if needed (Router, QueryClient, etc.)
  return <>{children}</>;
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
): RenderResult {
  return render(ui, { wrapper: TestProviders, ...options });
}

export function renderHookWithProviders<Result, Props>(
  hook: (initialProps: Props) => Result,
  options?: Omit<RenderHookOptions<Props>, 'wrapper'>
): RenderHookResult<Result, Props> {
  return renderHook(hook, { wrapper: TestProviders, ...options });
}

export * from '@testing-library/react';

