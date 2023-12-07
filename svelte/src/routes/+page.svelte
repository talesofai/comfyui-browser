<script lang="ts">
  import Tabs from './Tabs.svelte';
  import FilesList from "./FilesList.svelte";
  import CollectionsList from './CollectionsList.svelte';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let activeTab = 'outputs';
</script>

<Tabs bind:activeTab={activeTab} />

{#if activeTab === 'collections'}
  <CollectionsList {comfyUrl} />
{:else}
  <FilesList {comfyUrl} />
{/if}
