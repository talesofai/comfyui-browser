import { writable } from 'svelte/store';

export const imageWidth = writable(50);
export const comfyUrl = writable('');

export enum TableMode {
  Score,
  View,
}
export const mode = writable(TableMode.View);
