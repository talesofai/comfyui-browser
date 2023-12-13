<script lang="ts">
  import { onMount } from "svelte";
  import { onLoadWorkflow, onScroll, fetchFiles } from './utils';
  import type { FOLDER_TYPES } from './utils';
  import MediaShow from "./MediaShow.svelte";
  import type Toast from "./Toast.svelte";

  export let comfyUrl: string;
  export let folderType: FOLDER_TYPES;
  export let toast: Toast;
  export let folderPath: string = '';
  $: if (folderPath) {
    fetchFiles(folderType, comfyUrl, folderPath)
    .then(res => {
      files = res;
    });
  }

  let comfyApp: any;
  let files: Array<any> = [];
  let showCursor = 20;

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.app;

    files = await fetchFiles(folderType, comfyUrl, folderPath);
    window.addEventListener('scroll', () => { showCursor = onScroll(showCursor, files.length); });
  });

  async function onCollect(file: any) {
    const res = await fetch(comfyUrl + '/browser/collections', {
      method: 'POST',
      body: JSON.stringify({
        filename: file.name,
        folder_path: file.folder_path,
        folder_type: folderType,
      }),
    });

    toast.show(
      res.ok,
      'Added to collections',
      'Failed to add to collections. Please check the ComfyUI server.'
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

  async function onClickDir(dir: any) {
    folderPath = dir.path;
  }
</script>

<div class="grid grid-cols-4 lg:grid-cols-6 gap-2 bg-base-300">
  {#each files.slice(0, showCursor) as file}
    {#if ['dir', 'image', 'video', 'json'].includes(file.fileType)}
      <div class="bg-base-100">
        <div class="flex items-center">
          <MediaShow
            file={file}
            styleClass="w-full h-36"
            onClickDir={onClickDir}
          />
        </div>

        <p class="font-bold max-h-12 leading-6 overflow-auto">{file.name}</p>
        <p class="text-gray-500">{file.formattedDatetime}</p>
        <p class="text-gray-500">{file.formattedSize}</p>

        <div class="">
          {#if comfyApp}
            <button
              class="btn btn-link btn-sm p-0 no-underline text-accent"
              on:click={async () => await onLoadWorkflow(file, comfyApp, toast)}
            >Load</button>
          {/if}
          <button
            class="btn btn-link btn-sm p-0 no-underline text-accent"
            on:click={async () => await onCollect(file)}
          >Collect</button>
          <button
            class="btn btn-link btn-sm p-0 no-underline text-error"
            on:click={async () => await onDelete(file)}
          >Delete</button>
        </div>
      </div>
    {/if}
  {/each}
</div>
