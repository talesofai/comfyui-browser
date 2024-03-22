export function zip<T = unknown, U = unknown>(arr1: T[], arr2: U[]): [T, U][] {
  return Array.from({ length: arr1.length }).map((_, i) => [arr1[i], arr2[i]]);
}
