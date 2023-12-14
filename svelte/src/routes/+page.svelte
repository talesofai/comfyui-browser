<script lang="ts">
  import Navbar from './Navbar.svelte';
  import FilesTab from "./FilesTab.svelte";
  import CollectionsTab from './CollectionsTab.svelte';
  import SourcesTab from './SourcesTab.svelte';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let activeTab = 'outputs';
</script>

<Navbar bind:activeTab={activeTab} />

{#if activeTab === 'collections'}
  <CollectionsTab {comfyUrl} />
{:else if activeTab === 'outputs'}
  <FilesTab {comfyUrl} />
{:else}
  <SourcesTab {comfyUrl} />
{/if}
