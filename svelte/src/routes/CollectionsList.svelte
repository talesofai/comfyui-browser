<script lang="ts">
  import { onMount } from "svelte";
  import { fetchFiles, onScroll } from './utils';
  import MediaShow from "./MediaShow.svelte";
  import Toast from "./Toast.svelte";

  export let comfyUrl: string;

  let comfyApp: any;
  let files: Array<any> = [];
  let config: any = {};
  let configGitRepo = '';
  let showCursor = 20;
  let toast: Toast;

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.comfyApp;

    files = await fetchFiles('collections', comfyUrl);
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
    files = await fetchFiles('collections', comfyUrl);
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

  async function onClickLoad(file: any) {
    const res = await fetch(file.url);
    const blob = await res.blob();
    const fileObj = new File([blob], file.name, {
      type: res.headers.get('Content-Type') || '',
    });
    await comfyApp.handleFile(fileObj);
  }

  async function onDelete(file: any) {
    const ret = confirm('You will delete this file? ' + file.name);
    if (!ret) {
      return;
    }

    const res = await fetch(comfyUrl + '/browser/files', {
      method: 'DELETE',
      body: JSON.stringify({
        type: 'collections',
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
    const res = await fetch(comfyUrl + '/browser/collections/' + file.name, {
      method: 'PUT',
      body: JSON.stringify(payload),
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
      'Updated',
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
</script>

<div>
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

<ul class="space-y-2 bg-base-300">
  {#each files.slice(0, showCursor) as file}
    <li class="flex h-36 border-0 space-x-4 bg-base-100">
      <MediaShow {file} styleClass="w-36" />
      <div class="space-y-2 w-72">
        <input
          type="text"
          class="input-bordered font-bold w-full bg-base-100"
          on:blur={(e) => updateFilename(e, file)}
          value={file.name}
        />
        <p class="text-gray-500">
          {file.formattedDatetime} | {file.formattedSize}
        </p>

        <div>
          {#if comfyApp}
            <button
              class="btn btn-link btn-sm p-0 no-underline text-accent"
              on:click={async () => await onClickLoad(file)}
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

<Toast bind:this={toast} />
