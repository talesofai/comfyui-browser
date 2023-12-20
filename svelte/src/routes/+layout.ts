import { register, init, getLocaleFromNavigator } from 'svelte-i18n';

register('en-US', () => import('../i18n/en-US.json'));
register('zh-CN', () => import('../i18n/zh-CN.json'));

export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load({ url }) {
  init({
    fallbackLocale: 'zh-CN',
    initialLocale: getLocaleFromNavigator(),
  });

  let comfyUrl = '';
  if (typeof process === 'undefined') {
    comfyUrl = url.searchParams.get('comfyUrl') || '';
  }

  return {
    comfyUrl,
  };
}
