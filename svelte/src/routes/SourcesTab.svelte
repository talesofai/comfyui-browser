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

  function onClickSource(source: any) {
    selectedSource = source;
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
          class="btn"
          on:click={() => onClickSource(source)}
        >{source.name}</button>
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
