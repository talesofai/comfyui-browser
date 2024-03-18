import { waitLocale } from 'svelte-i18n';

/** @type {import('./$types').PageLoad} */
export async function load({ url }) {
  await waitLocale();
    const path = url.searchParams.get("path") 
    return {
      path,
    };
  }
  