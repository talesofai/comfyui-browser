<script lang="ts">
  import { onMount } from "svelte";
  import Toast from "./Toast.svelte";
  import FilesList from "./FilesList.svelte";

  export let comfyUrl: string;

  let sources: Array<any> = [];
  let toast: Toast;
  let selectedSource: any;
  let sourceEditModal: any;
  let inputRepoUrl: string;
  let addWaiting = false;

  async function refreshSources(selectGitUrl: string | null = null) {
    const res = await fetch(comfyUrl + '/browser/sources');
    const ret = await res.json();
    sources = ret.sources;

    if (selectGitUrl) {
      selectGitUrl = selectGitUrl.trim();
      selectedSource = sources.find(s => s.url == selectGitUrl);
    }

    if (! selectedSource) {
      selectedSource = sources[0];
    }
  }

  onMount(async () => {
    await refreshSources();
  });

  function onClickAddSource(source: any) {
    selectedSource = source;
  }

  async function onClickDeleteSource(source: any) {
    const ret = confirm('You want to delete this source? ' + source.name);
    if (!ret) {
      return;
    }

    const res = await fetch(comfyUrl + `/browser/sources/${source.name}`, {
      method: 'DELETE',
    });

    if (res.ok) {
      await refreshSources();
    }
    toast.show(
      res.ok,
      'Deleted this source',
      'Failed to delete this source. Please check the ComfyUI server.',
    );
  }

  function openEditModal() {
    sourceEditModal.show();
  }

  async function addSource() {
    if (! inputRepoUrl) {
      toast.show(false, '', 'missing Git URL', 1000);
      return;
    }

    addWaiting = true;
    const res = await fetch(comfyUrl + '/browser/sources', {
      method: 'POST',
      body: JSON.stringify({
        repo_url: inputRepoUrl,
      }),
    });
    addWaiting = false;

    if (res.ok) {
      await refreshSources(inputRepoUrl);
    }
    toast.show(
      res.ok,
      'Added a new source',
      'Failed to add a new source. Please check the ComfyUI server.',
    );
    sourceEditModal.close();
  }
</script>

<div>
  <ul class="inline-block menu bg-base-200 w-56 p-0 [&_li>*]:rounded-none">
    <li>
      <button
        class="btn"
        on:click={openEditModal}
      >Add new source</button>
    </li>
    {#each sources as source}
      <li>
        <button
          class="btn inline-block w-3/4"
          on:click={() => onClickAddSource(source)}
        >{source.name}</button>
        <button
          class="btn inline-block w-1/4"
          on:click={() => onClickDeleteSource(source)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </li>
    {/each}
  </ul>

  <div class="inline-block w-auto">
    <FilesList
      folderType="sources"
      folderPath={selectedSource?.name}
      comfyUrl={comfyUrl}
      toast={toast}
    />
  </div>
</div>

<Toast bind:this={toast} />

<!-- Open the modal using ID.showModal() method -->
<dialog class="modal" bind:this={sourceEditModal}>
  <div class="modal-box">
    <input
      type="text"
      bind:value={inputRepoUrl}
      placeholder="Input Git remote address of the source"
      class="input input-bordered w-full max-w-xs"
    />
    <button
      class="btn"
      on:click={addSource}
      disabled={addWaiting}
    >{addWaiting ? 'Adding...' : 'Add'}</button>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
