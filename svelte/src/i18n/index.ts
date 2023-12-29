import { browser } from '$app/environment';
import { locale, register, init, getLocaleFromNavigator } from 'svelte-i18n';

register('en-US', () => import('./en-US.json'));
register('zh-CN', () => import('./zh-CN.json'));

const langKey = 'lang';
const defaultLocale = 'en-US';

let initialLocale: string | null = browser ? window.navigator.language : defaultLocale;
if (getLocaleFromNavigator()) {
  initialLocale = getLocaleFromNavigator();
}
if (browser && localStorage.getItem(langKey)) {
  initialLocale = localStorage.getItem(langKey);
}

init({
  fallbackLocale: defaultLocale,
  initialLocale: initialLocale,
  handleMissingMessage: (input: any) => input.id.split('.').pop(),
});

locale.subscribe((value: any) => {
  //console.log('changed lang to ', value);

  if (browser) {
    localStorage.setItem(langKey, value);
  }
});
