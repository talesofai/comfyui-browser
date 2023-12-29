<script lang="ts">
  import { onMount } from 'svelte';
  import { t } from 'svelte-i18n';
  import { fetchFiles, onLoadWorkflow, onScroll } from './utils';
  import MediaShow from './MediaShow.svelte';
  import Toast from './Toast.svelte';

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
    fetchFiles(folderType, comfyUrl, folderPath).then((res) => {
      files = res;
      loaded = true;
    });
  }

  $: try {
    searchRegex = new RegExp(searchQuery.toLowerCase());
  } catch {
    searchRegex = new RegExp('');
  }

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.app;

    folderPath = '';
    config = (await fetchConfig()) || {};
    configGitRepo = config?.git_repo;

    window.addEventListener('scroll', () => {
      showCursor = onScroll(showCursor, files.length);
    });
  });

  async function fetchConfig() {
    const res = await fetch(comfyUrl + '/browser/config');
    return await res.json();
  }

  async function onClickSyncCollections(e: Event) {
    const btn = e.target as HTMLButtonElement;
    btn.disabled = true;
    btn.innerHTML = $t('collectionsTab.btn.syncing');
    const res = await fetch(comfyUrl + '/browser/collections/sync', {
      method: 'POST',
    });

    toast.show(
      res.ok,
      $t('collectionsTab.toast.synced'),
      $t('collectionsTab.toast.syncFailed'),
    );
    btn.disabled = false;
    btn.innerHTML = $t('collectionsTab.btn.sync');

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
      $t('collectionsTab.toast.configUpdated'),
      $t('collectionsTab.toast.configUpdatedFailed'),
    );
  }

  async function onDelete(file: any) {
    const ret = confirm($t('collectionsTab.toast.deleteConfirm') + file.name);
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
      $t('collectionsTab.toast.deleteSuccess') + file.name,
      $t('collectionsTab.toast.deleteFailed'),
    );
    files = files.filter((f) => f != file);
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
      $t('collectionsTab.toast.updated'),
      $t('collectionsTab.toast.updatedFailed'),
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
      $t('collectionsTab.toast.updated'),
      $t('collectionsTab.toast.updatedFailed'),
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

    folderPath = folderPath
      .split('/')
      .slice(0, index + 1)
      .join('/');
  }
</script>

<div class="flex border-b border-base-content pb-2">
  <a
    class="btn pr-2"
    target="_blank"
    href="https://github.com/talesofai/comfyui-browser/wiki/How-to-use-Sync-in-the-Saves-tab"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      data-slot="icon"
      class="w-6 h-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
      />
    </svg>
  </a>
  <input
    type="text"
    placeholder={$t('collectionsTab.syncInput.placeholder')}
    bind:value={configGitRepo}
    class="input input-bordered w-full max-w-lg"
  />
  {#if configGitRepo != config?.git_repo}
    <button class="btn btn-outline btn-accent" on:click={onClickSaveConfig}>
      {$t('collectionsTab.btn.save')}
    </button>
  {/if}
  <button class="btn btn-outline btn-accent" on:click={onClickSyncCollections}>
    {$t('collectionsTab.btn.sync')}
  </button>
</div>

<div class="max-w-full text-sm breadcrumbs flex flex-row ml-4">
  <ul class="basis-2/3">
    <li>
      <button on:click={() => onClickPath(-1)}>{$t('common.rootDir')}</button>
    </li>
    {#each (folderPath || '').split('/') as path, index}
      <li><button on:click={() => onClickPath(index)}>{path}</button></li>
    {/each}
  </ul>

  <input
    type="text"
    placeholder={$t('collectionsTab.searchInput.placeholder')}
    bind:value={searchQuery}
    class="input input-bordered border-slate-600 w-full h-full rounded-none text-sm basis-1/3"
  />
</div>

<ul class="space-y-2">
  {#each files
    .filter((f) => searchRegex.test(f.name.toLowerCase()) || searchRegex.test(f.notes.toLowerCase()))
    .slice(0, showCursor) as file}
    <li class="flex h-16 sm:h-28 border-0 space-x-4 p-2 bg-info-content">
      <MediaShow {file} styleClass="w-16 sm:w-28" {onClickDir} />
      <div class="space-y-2 w-96 relative">
        <input
          type="text"
          class="input-bordered font-bold w-full bg-base-100"
          on:blur={(e) => updateFilename(e, file)}
          value={file.name}
        />
        <p class="text-gray-500 text-xs hidden sm:block">
          {file.formattedDatetime} | {file.formattedSize}
        </p>

        <div class="bottom-0 absolute">
          {#if comfyApp && file.type != 'dir'}
            <button
              class="btn btn-link btn-sm p-0 no-underline text-accent"
              on:click={async () => await onLoadWorkflow(file, comfyApp, toast)}
              >{$t('common.btn.load')}</button
            >
          {/if}
          <button
            class="btn btn-link btn-sm p-0 no-underline text-error ml-52"
            on:click={async () => await onDelete(file)}
          >
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 2v4h6v2h-2v14H4V8H2V6h6V2h8zm-2 2h-4v2h4V4zm0 4H6v12h12V8h-4zm-5 2h2v8H9v-8zm6 0h-2v8h2v-8z" fill="#f77"/>
            </svg>
            {$t('common.btn.delete')}
        </button>
        </div>
      </div>

      <div>
        <textarea
          name="notes"
          placeholder={$t('collectionsTab.collection.memoPlaceholder')}
          on:blur={(e) => updateFileNotes(e, file)}
          class="resize-none textarea hidden md:block md:w-72 max-w-72 h-14 sm:h-24"
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
        {$t('common.emptyList')}
      {:else}
        {$t('common.rootDir')}
      {/if}
    </span>
  </div>
{/if}

<Toast bind:this={toast} />
