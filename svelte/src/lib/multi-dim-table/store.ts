import { writable } from 'svelte/store';
import PubSub from 'pubsub-js';

export const imageWidth = writable(50);
export const comfyUrl = writable('');

export enum TableMode {
  Score,
  View,
}
export const mode = writable(TableMode.View);

export function createRefetchStatisticPublisher() {
  return () => PubSub.publish('refetch-statistics');
}

export function createRefetchStatisticSubscriber(fn: () => void) {
  return PubSub.subscribe('refetch-statistics', fn);
}
