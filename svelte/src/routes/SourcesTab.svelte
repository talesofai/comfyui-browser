<script lang="ts">
  import { onMount } from "svelte";
  import Toast from "./Toast.svelte";
  import FilesList from "./FilesList.svelte";

  export let comfyUrl: string;

  let sources: Array<any> = [];
  let toast: Toast;
  let sourceEditModal: any;
  let inputRepoUrl: string;
  let waitingForUrl: string = '';
  let folderPath = '';
  let allSources: Array<any> = [];
  let fileList: FilesList;
  let syncingSouce: any;

  async function refreshSources() {
    const res = await fetch(comfyUrl + '/browser/sources');
    const ret = await res.json();
    sources = ret.sources;
  }

  onMount(async () => {
    refreshSources();
    getAllSources();
  });

  function onClickSource(source: any) {
    console.log(folderPath);
    folderPath = source.name;
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
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      'Deleted this source',
      'Failed to delete this source. Please check the ComfyUI server.',
    );
  }

  async function onClickSyncSource(source: any) {
    syncingSouce = source;
    const res = await fetch(comfyUrl + `/browser/sources/sync/${source.name}`, {
      method: 'POST',
    });
    syncingSouce = null;

    if (res.ok) {
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      'Synced ' + [source.author, source.name].join('/'),
      'Failed to sync this source. Please check the ComfyUI server.',
    );
  }

  function openEditModal() {
    sourceEditModal.showModal();
  }

  async function addSource(url: string) {
    if (! url) {
      toast.show(false, '', 'missing Git URL');
      return;
    }

    waitingForUrl = url;
    const res = await fetch(comfyUrl + '/browser/sources', {
      method: 'POST',
      body: JSON.stringify({
        repo_url: url,
      }),
    });
    waitingForUrl = '';

    if (res.ok) {
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      'Added a new source',
      'Failed to add a new source. Please check the ComfyUI server.',
    );
    sourceEditModal.close();
  }

  async function getAllSources() {
    const res = await fetch(comfyUrl + '/browser/sources/all');
    const ret = await res.json();
    allSources = ret.sources;
  }
</script>

<div class="drawer md:drawer-open">
  <input type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col pl-2">
    <FilesList
      folderType="sources"
      bind:folderPath={folderPath}
      comfyUrl={comfyUrl}
      toast={toast}
      bind:this={fileList}
    />
  </div>

  <div class="drawer-side border-r border-base-content pr-2">
    <ul class="menu bg-base-200 w-56 p-0 [&_li>*]:rounded-none">
      <li>
        <button class="btn-outline btn-accent" on:click={openEditModal}>Add new source</button>
      </li>

      {#each sources as source}
        <li class="h-14">
          <button
            class="h-14 line-clamp-2 overflow-hidden {source.name == folderPath.split('/')[0] ? 'active' : ''}"
            on:click={() => onClickSource(source)}
          ><p class="w-40 truncate whitespace-normal">{source.name}</p></button>
          <button
            class="h-14 right-0 fixed flex items-center justify-center"
            on:click={() => onClickSyncSource(source)}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
              class="{syncingSouce == source ? 'text-accent' : ''} w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </button>
        </li>
      {/each}
    </ul>
  </div>
</div>

<Toast bind:this={toast} />

<!-- Open the modal using ID.showModal() method -->
<dialog class="modal" bind:this={sourceEditModal}>
  <div class="modal-box w-5/6 max-w-5xl">
    <div class="mb-2 flex space-x-2">
      <input
        type="text"
        bind:value={inputRepoUrl}
        placeholder="https://github.com/comfyanonymous/ComfyUI_examples"
        class="grow input input-bordered"
      />
      <button
        class="btn btn-outline btn-primary"
        on:click={() => addSource(inputRepoUrl)}
        disabled={waitingForUrl.length > 0 || !inputRepoUrl}
      >{waitingForUrl === inputRepoUrl && inputRepoUrl ? 'Subscribing...' : 'Subscribe'}</button>
    </div>

    <div>
      {#if allSources.length === 0}
        <div class="w-full h-full flex items-center justify-center">
          <span class="font-bold text-4xl">
            Loading ...
          </span>
        </div>
      {/if}
      <ul class="space-y-1">
        {#each allSources as s}
          <li class="flex flex-nowrap space-x-2 h-20 border-b border-b-base-content">
            <img
              src={`https://github.com/${s.author}.png`}
              alt={s.author} />
            <div class="w-80">
              <a class="link link-warning text-lg no-underline" href={s.url} target="_blank">
                <p>{s.author}/{s.title}</p>
              </a>
              <a href={s.url} target="_blank">
                <p class="text-xs text-gray-500">{s.url}</p>
              </a>
            </div>
            <div class="w-72 grow">
              <p>{s.description}</p>
            </div>
            <div class="flex items-center justify-center">
              <button
                class="btn btn-outline btn-primary no-underline text-accent"
                on:click={() => addSource(s.url)}
                disabled={waitingForUrl.length > 0}
              >
                {waitingForUrl === s.url ? 'Subscribing...' : 'Subscribe'}
              </button>
            </div>
          </li>
        {/each}
      </ul>
    </div>
    <p class="mt-1 text-xs text-gray-500">
      You could open
      <a class="text-accent" target="_blank" href="https://github.com/talesofai/comfyui-browser/edit/main/data/sources.json">
        a pull request
      </a>
      or submit
      <a class="text-accent" target="_blank" href="https://github.com/talesofai/comfyui-browser/issues/new?assignees=tzwm&labels=workflow-repo&projects=&template=new-workflow-repository.md&title=New+workflow+repo%3A">
        an issue
      </a>
      to add your workflow repository here.<br />
      Thank you to everyone who contributes to the open community!
    </p>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
