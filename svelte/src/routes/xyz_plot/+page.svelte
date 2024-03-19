<script>
  import { onMount } from 'svelte';
  import MultiDimTable from '$lib/multi-dim-table/layout.svelte';
  import AnalyzeTable from '$lib/multi-dim-table/table.svelte';
  import { imageWidth } from '$lib/multi-dim-table/store';
  import InfoIcon from '$lib/icons/info.svelte';

  /** @type {import('./$types').PageData} */
  export let data;

  /** @type {string | null} */
  export let path;

  $: ({ path } = data);

  let mounted = false;

  /** @type {import("$lib/multi-dim-table/models").Payload}*/
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
    <MultiDimTable
      extraItems={[
        {
          label: 'Open Workflow',
          onClick: () => {
            open(payload.workflow.url);
          },
        },
      ]}
    >
      <div slot="title">
        XYZ Plots

        <div
          class="tooltip tooltip-bottom z-10 before:whitespace-pre-wrap"
          data-tip={payload.annotations
            .map((d) => `${d.axis}: ${d.key} - ${d.type}`)
            .join('\n')}
        >
          <InfoIcon />
        </div>
      </div>
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
    </MultiDimTable>
  {/if}
{:else}
  Invalid Path
{/if}
