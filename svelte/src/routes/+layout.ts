import '../i18n/index';
import { waitLocale } from 'svelte-i18n';

export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load({ url }) {
  await waitLocale();

  let comfyUrl = '';
  if (typeof process === 'undefined') {
    comfyUrl = url.searchParams.get('comfyUrl') || '';
  }

  return {
    comfyUrl,
  };
}
