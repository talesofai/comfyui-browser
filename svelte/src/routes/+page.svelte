<script lang="ts">
  import Tabs from './Tabs.svelte';
  import FilesList from "./FilesList.svelte";
  import CollectionsList from './CollectionsList.svelte';
  import { onMount } from 'svelte';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  const tabList = ['collections', 'files'];
  let activeTab = 'outputs';

  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const currentTab = urlParams.get('tab');
    if (currentTab && tabList.includes(currentTab)) {
      activeTab = currentTab;
    }
  });
</script>

<Tabs bind:activeTab={activeTab} />

{#if activeTab === 'collections'}
  <CollectionsList {comfyUrl} />
{:else}
  <FilesList {comfyUrl} />
{/if}
