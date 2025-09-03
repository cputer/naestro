export type Route = 'local' | 'cloud';

export interface RouteDecision {
  tokens: number;
  longContextThreshold?: number;
  localAvailable?: boolean;
}

export function chooseRoute({
  tokens,
  longContextThreshold = 200000,
  localAvailable = true
}: RouteDecision): Route {
  if (tokens > longContextThreshold) {
    return 'cloud';
  }
  return localAvailable ? 'local' : 'cloud';
}
