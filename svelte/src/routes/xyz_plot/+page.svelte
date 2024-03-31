<script>
  import { onMount } from 'svelte';
  import MultiDimTableLayout from '$lib/multi-dim-table/layout.svelte';
  import AnalyzeTable from '$lib/multi-dim-table/table.svelte';
  import {
    comfyUrl,
    createRefetchStatisticPublisher,
  } from '$lib/multi-dim-table/store';
  import InfoIcon from '$lib/icons/info.svelte';
  import { db, getUser } from '$lib/db';
  import { v1 as uuid } from 'uuid';
  import { fakeUsername } from '$lib/random';
  import { createRefetchStatisticSubscriber } from '$lib/multi-dim-table/store';

  /** @type {import('./$types').PageData} */
  export let data;

  /** @type {string | null} */
  export let path;

  /** @type {import('$lib/multi-dim-table/models').AxisScore[]} */
  let scores;

  $: ({ path } = data);
  $: comfyUrl.set(data.comfyUrl);

  let mounted = false;

  /** @type {import("$lib/multi-dim-table/models").Payload}*/
  let payload;
  let loading = false;

  /**@type {HTMLElement | undefined}*/
  let tableContainerRef;

  createRefetchStatisticSubscriber(() => {
    fetch(data.comfyUrl + '/browser/xyz_plot/statistic?path=' + data.path)
      .then(async (d) => {
        if (d.ok) {
          scores = await d.json().then((d) => d.result);
        }
      })
      .catch(() => {});
  });
  const refetch = createRefetchStatisticPublisher();

  $: {
    if (mounted && path) {
      loading = true;
      fetch(path)
        .then((d) => d.json())
        .then((d) => (payload = d))
        .finally(() => {
          loading = false;
        });
    }
  }

  $: {
    if (mounted && path) {
      refetch();
    }
  }

  onMount(async () => {
    mounted = true;
    const user = await getUser();
    if (!user) {
      db.user.add({
        uuid: uuid(),
        name: fakeUsername(),
        ctime: Date.now(),
        mtime: Date.now(),
      });
    }
  });
</script>

{#if typeof data.path === 'string' && data.path.length > 0}
  {#if loading}
    <div class="flex flex-col w-screen h-screen justify-center items-center">
      <span class="loading loading-dots loading-lg"></span>
    </div>
  {:else if !payload}
    null
  {:else}
    <MultiDimTableLayout
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
        XYZ Plot
        <div
          class="tooltip before:pl-20 before:text-left before:max-w-96 tooltip-bottom z-40 before:whitespace-pre-wrap"
          data-tip={payload.annotations
            .map((d) => `${d.axis}: ${d.key} - ${d.type}`)
            .join('\n')}
        >
          <InfoIcon />
        </div>
      </div>
      <div class="w-full h-full" bind:this={tableContainerRef}>
        <AnalyzeTable
          bind:payload
          bind:scores
          height={tableContainerRef?.clientHeight ?? 0}
        />
      </div>
    </MultiDimTableLayout>
  {/if}
{:else}
  Invalid Path
{/if}
