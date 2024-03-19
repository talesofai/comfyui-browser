import { waitLocale } from 'svelte-i18n';

/** @type {import('./$types').PageLoad} */
export async function load({ url }) {
  await waitLocale();

  if (typeof process === 'undefined') {
    const path = url.searchParams.get('path');
    return {
      path,
    };
  }
  return {};
}
