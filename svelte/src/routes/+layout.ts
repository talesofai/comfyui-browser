export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load({ url }) {
  let comfyUrl = '';
  if (typeof process === 'undefined') {
    comfyUrl = url.searchParams.get('comfyUrl') || '';
  }

  return {
    comfyUrl,
  }
}
