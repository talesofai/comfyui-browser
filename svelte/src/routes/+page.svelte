<script lang="ts">
  import Navbar from './Navbar.svelte';
  import FilesTab from './FilesTab.svelte';
  import CollectionsTab from './CollectionsTab.svelte';
  import SourcesTab from './SourcesTab.svelte';
  import ModelsTab from './ModelsTab.svelte';
  import { getLocalConfig } from './utils';
  import { onMount } from 'svelte';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let activeTab = 'outputs';

  onMount(() => {
    const config = getLocalConfig();
    if (config.lastTab) {
      activeTab = config.lastTab;
    }
  });
</script>

<Navbar bind:activeTab />

{#if activeTab === 'collections'}
  <CollectionsTab {comfyUrl} />
{:else if activeTab === 'sources'}
  <SourcesTab {comfyUrl} />
{:else if activeTab === 'models'}
  <ModelsTab {comfyUrl} />
{:else}
  <FilesTab {comfyUrl} />
{/if}
