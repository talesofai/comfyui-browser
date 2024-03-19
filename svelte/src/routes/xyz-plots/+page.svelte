<script>
  import { onMount } from 'svelte';
  import AnalyzeLayout from '$lib/analyze/layout.svelte';
  import AnalyzeTable from '$lib/analyze/table.svelte';
  import { imageWidth } from '$lib/analyze/store';
  /** @type {import('./$types').PageData} */
  export let data;

  /** @type {string | null} */
  export let path;

  $: ({ path } = data);

  let mounted = false;

  /** @type {import("$lib/analyze/models").Payload}*/
  let payload;
  let loading = false;

  /**@type {HTMLElement | undefined}*/
  let tableContainerRef;

  $: {
    if (mounted && path !== null) {
      loading = true;
      fetch(path)
        .then((d) => d.json())
        .then((d) => (payload = d))
        .finally(() => {
          loading = false;
        });
    }
  }

  onMount(() => {
    mounted = true;
  });

  let _imageWidth = 50;

  $: {
    imageWidth.set(_imageWidth);
  }
</script>

{#if typeof data.path === 'string' && data.path.length > 0}
  {#if loading}
    <div class="flex flex-col w-screen h-screen justify-center items-center">
      <span class="loading loading-dots loading-lg"></span>
    </div>
  {:else if !payload}
    null
  {:else}
    <AnalyzeLayout
      extraItems={[
        {
          label: 'Open Workflow',
          onClick: () => {
            open(payload.workflow.url);
          },
        },
      ]}
      sidebarItems={payload.annotations.map((d) => ({
        label: `${d.axis}: ${d.key} - ${d.type}`,
      }))}
    >
      <div slot="title">Analyze</div>
      <li slot="extra">
        <div>
          <input
            type="range"
            min="5"
            max="300"
            bind:value={_imageWidth}
            class="range"
          />
        </div>
      </li>
      <div class="w-full h-full" bind:this={tableContainerRef}>
        <AnalyzeTable {payload} height={tableContainerRef?.clientHeight ?? 0} />
      </div>
    </AnalyzeLayout>
  {/if}
{:else}
  Invalid Path
{/if}
