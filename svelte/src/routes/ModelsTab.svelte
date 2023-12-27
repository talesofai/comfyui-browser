<script lang="ts">
  import DownloadHistory from "./DownloadHistory.svelte";
  import NewDownload from "./NewDownload.svelte";

  export let comfyUrl: string;

  let activeTab = 'downloadNewModel';

  $: activeTabClass = function(tab: string) {
    return tab === activeTab ? 'active' : '';
  }

  async function onClickTab(tab: string) {
    activeTab = tab;
  }
</script>

<div class="drawer md:drawer-open">
  <input type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col pl-2">
    {#if activeTab === 'downloadHistory'}
      <DownloadHistory {comfyUrl} />
    {:else}
      <NewDownload
        comfyUrl={comfyUrl}
        afterStartingDownload={() => onClickTab('downloadHistory')}
      />
    {/if}
  </div>

  <div class="drawer-side border-r border-base-content pr-2">
    <ul class="menu bg-base-200 w-56 p-0 [&_li>*]:rounded-none">
      <li  class="h-10">
        <button
          class="{activeTabClass('downloadNewModel')} pl-2 btn-outline btn-accent"
          on:click={() => onClickTab('downloadNewModel')}
        >
          Download new model
        </button>
      </li>
      <li  class="h-10">
        <button
          class="{activeTabClass('downloadHistory')} pl-2 btn-outline btn-accent"
          on:click={() => onClickTab('downloadHistory')}
        >
          Download History
        </button>
      </li>
    </ul>
  </div>
</div>
