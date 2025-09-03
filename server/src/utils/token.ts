export type TextInput = string | string[];

export function estimateTokens(input: TextInput): number {
  const text = Array.isArray(input) ? input.join(' ') : input;
  if (!text.trim()) {
    return 0;
  }
  return text.trim().split(/\s+/).length;
}
