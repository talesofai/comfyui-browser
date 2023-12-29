<script lang="ts">
  import { setLocalConfig } from './utils';
  import { t, locales, locale } from 'svelte-i18n';

  export let activeTab = 'outputs';

  $: activeTabClass = function (tab: string) {
    return tab === activeTab ? 'active' : '';
  };

  async function onClickTab(tab: string) {
    activeTab = tab;

    setLocalConfig('lastTab', tab);
  }

  function showLocale(locale: string) {
    switch (locale.split('-')[0]) {
      case 'en':
        return 'En';
      case 'zh':
        return '中文';
      default:
        return 'En';
    }
  }
</script>

<div class="flex">
  <ul class="menu menu-horizontal bg-base-200 rounded-box flex-1">
    <li>
      <button
        class={activeTabClass('outputs')}
        on:click={() => onClickTab('outputs')}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
          />
        </svg>
        {$t('navbar.outputs')}
      </button>
    </li>

    <li>
      <button
        class={activeTabClass('collections')}
        on:click={() => onClickTab('collections')}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z"
          />
        </svg>
        {$t('navbar.saves')}
      </button>
    </li>
    <li>
      <button
        class={activeTabClass('sources')}
        on:click={() => onClickTab('sources')}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12.75 19.5v-.75a7.5 7.5 0 00-7.5-7.5H4.5m0-6.75h.75c7.87 0 14.25 6.38 14.25 14.25v.75M6 18.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0z"
          />
        </svg>
        {$t('navbar.sources')}
      </button>
    </li>
    <li>
      <button
        class="{activeTabClass('models')}"
        on:click={() => onClickTab('models')}
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
        </svg>
        Models
      </button>
    </li>
  </ul>

  <div class="dropdown dropdown-hover">
    <div tabindex="0" role="button" class="m-1 btn btn-ghost">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802" />
      </svg>
      <svg width="12px" height="12px" class="hidden h-2 w-2 fill-current opacity-60 sm:inline-block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048">
        <path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
      </svg>
    </div>
    <ul class="p-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-52">
       {#each $locales as l}
         <li class="w-20">
           <button class={l == $locale ? 'active' : ''} on:click={() => locale.set(l)}>
             {showLocale(l)}
           </button>
         </li>
       {/each}
    </ul>
  </div>
  <div class="hidden sm:flex flex-0 items-center justify-center p-2">
    <a href="https://github.com/talesofai/comfyui-browser" target="_blank">
      <img
        src="https://img.shields.io/github/stars/talesofai/comfyui-browser?style=social"
        alt="stars - comfyui-browser"
      />
    </a>
  </div>
</div>
