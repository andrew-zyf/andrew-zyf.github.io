// Time-based damping keeps gestures consistent across display refresh rates.
export const damp = (dt: number, duration: number) => 1 - Math.exp(-dt / duration);
export const zoomStep = (current: number, target: number, dt: number) =>
  current * Math.exp(Math.log(target / current) * damp(dt, 95));

export function inertiaStep(velocity: number, dt: number) {
  const decay = Math.exp(-dt / 220);
  return { distance: velocity * 220 * (1 - decay), velocity: velocity * decay };
}
