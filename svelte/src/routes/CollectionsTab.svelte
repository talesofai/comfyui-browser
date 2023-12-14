<script lang="ts">
  import { onMount } from "svelte";
  import { fetchFiles, onLoadWorkflow, onScroll } from './utils';
  import MediaShow from "./MediaShow.svelte";
  import Toast from "./Toast.svelte";

  export let comfyUrl: string;

  const folderType = 'collections';

  let comfyApp: any;
  let files: Array<any> = [];
  let config: any = {};
  let configGitRepo = '';
  let showCursor = 20;
  let toast: Toast;
  let folderPath: string;
  let loaded: boolean = false;
  let searchQuery = '';
  let searchRegex = new RegExp('');

  $: if (folderPath != undefined) {
    fetchFiles(folderType, comfyUrl, folderPath)
    .then(res => {
      files = res;
      loaded = true;
    });
  }


  $: try {
    searchRegex = new RegExp(searchQuery.toLowerCase());
  } catch {
    searchRegex =  new RegExp('');
  }


  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.app;

    folderPath = '';
    config = await fetchConfig() || {};
    configGitRepo = config?.git_repo;

    window.addEventListener('scroll', () => { showCursor = onScroll(showCursor, files.length); });
  });

  async function fetchConfig() {
    const res = await fetch(comfyUrl + '/browser/config');
    return await res.json();
  }

  async function onClickSyncCollections(e: Event) {
    const btn = e.target as HTMLButtonElement;
    btn.disabled = true;
    btn.innerHTML = 'Syncing...';
    const res = await fetch(comfyUrl + '/browser/collections/sync', {
     method: 'POST',
    });

    toast.show(
      res.ok,
      'Synced',
      'Failed to sync. Please check the ComfyUI server.'
    );
    btn.disabled = false;
    btn.innerHTML = 'Sync';

    folderPath = '';
    files = await fetchFiles(folderType, comfyUrl);
  }

  async function onClickSaveConfig() {
    const res = await fetch(comfyUrl + '/browser/config', {
      method: 'PUT',
      body: JSON.stringify({
        git_repo: configGitRepo,
      }),
    });

    toast.show(
      res.ok,
      'Updated config',
      'Failed to update config. Please check the ComfyUI server.'
    );
  }

  async function onDelete(file: any) {
    const ret = confirm('You want to delete this file? ' + file.name);
    if (!ret) {
      return;
    }

    const res = await fetch(comfyUrl + '/browser/files', {
      method: 'DELETE',
      body: JSON.stringify({
        folder_type: folderType,
        filename: file.name,
        folder_path: file.folder_path,
      }),
    });

    toast.show(
      res.ok,
      'Deleted the file ' + file.name,
      'Failed to delete the file. Please check the ComfyUI server.'
    );
    files = files.filter(f => f != file);
  }

  async function updateFile(file: any, payload: any) {
    const res = await fetch(comfyUrl + '/browser/files', {
      method: 'PUT',
      body: JSON.stringify({
        folder_type: folderType,
        folder_path: file.folder_path,
        filename: file.name,
        new_data: payload,
      }),
    });

    return res.ok;
  }

  async function updateFilename(e: Event, file: any) {
    //@ts-ignore
    const value = e.target.value;
    if (value === file.name) {
      return;
    }

    const ret = await updateFile(file, {
      filename: value,
      notes: file.notes || '',
      folder_path: file.folder_path,
    });

    toast.show(
      ret,
      'Memos Updated',
      'Failed to update. Please check the ComfyUI server.'
    );
  }

  async function updateFileNotes(e: Event, file: any) {
    //@ts-ignore
    const value = e.target.value;
    if (value == file.notes) {
      return;
    }

    const ret = await updateFile(file, {
      filename: file.name,
      notes: value,
      folder_path: file.folder_path,
    });

    toast.show(
      ret,
      'Updated',
      'Failed to update. Please check the ComfyUI server.'
    );
  }

  async function onClickDir(dir: any) {
    folderPath = dir.path;
  }

  async function onClickPath(index: number) {
    if (index === -1) {
      folderPath = '';
      return;
    }

    folderPath = folderPath.split('/').slice(0, index + 1).join('/');
  }
</script>

<div class="border-b-2 border-slate-700 pb-2">
  <input
    type="text"
    placeholder="Input your git repository address"
    bind:value={configGitRepo}
    class="input input-bordered w-full max-w-lg"
  />
  {#if configGitRepo != config?.git_repo}
    <button
      class="btn btn-outline btn-accent"
      on:click={onClickSaveConfig}
    >
      Save
    </button>
  {/if}
  <button
    class="btn btn-outline btn-accent"
    on:click={onClickSyncCollections}
  >
    Sync
  </button>
</div>

<div class="max-w-full text-sm breadcrumbs flex flex-row ml-4">
  <ul class="basis-2/3">
    <li><button on:click={() => onClickPath(-1)}>Root</button></li>
    {#each (folderPath || '').split('/') as path, index}
      <li><button on:click={() => onClickPath(index)}>{path}</button></li>
    {/each}
  </ul>

  <input
    type="text"
    placeholder="Filter by filename or memos"
    bind:value={searchQuery}
    class="input input-bordered border-slate-600 w-full h-full rounded-none text-sm basis-1/3"
  />
</div>

<ul class="space-y-2">
  {#each files.filter(f => searchRegex.test(f.name.toLowerCase()) || searchRegex.test(f.notes.toLowerCase()))
    .slice(0, showCursor) as file}
    <li class="flex h-36 border-0 space-x-4 p-2 bg-base-300">
      <MediaShow
        file={file}
        styleClass="w-36"
        onClickDir={onClickDir}
      />
      <div class="space-y-2 w-96 relative">
        <input
          type="text"
          class="input-bordered font-bold w-full bg-base-100"
          on:blur={(e) => updateFilename(e, file)}
          value={file.name}
        />
        <p class="text-gray-500 text-xs">
          {file.formattedDatetime} | {file.formattedSize}
        </p>

        <div class="bottom-0 absolute">
          {#if comfyApp && file.type != 'dir'}
            <button
              class="btn btn-link btn-sm p-0 no-underline text-accent"
              on:click={async () => await onLoadWorkflow(file, comfyApp, toast)}
            >Load</button>
          {/if}
          <button
            class="btn btn-link btn-sm p-0 no-underline text-error"
            on:click={async () => await onDelete(file)}
          >Remove</button>
        </div>
      </div>

      <div>
        <textarea
          name="notes"
          cols="40"
          rows="4"
          placeholder="write some memos..."
          on:blur={(e) => updateFileNotes(e, file)}
          class="resize-none textarea"
          value={file.notes}
        />
      </div>
    </li>
  {/each}
</ul>

{#if files.length === 0}
  <div class="w-full h-full flex items-center justify-center">
    <span class="font-bold text-4xl">
      {#if loaded}
        It's empty here.
      {:else}
        Loading ...
      {/if}
    </span>
  </div>
{/if}

<Toast bind:this={toast} />
