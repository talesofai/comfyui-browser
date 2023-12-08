<script lang="ts">
  import { onMount } from "svelte";
  import { fetchFiles, onScroll } from './utils';
  import MediaShow from "./MediaShow.svelte";
  import Toast from "./Toast.svelte";

  export let comfyUrl: string;

  let comfyApp: any;
  let files: Array<any> = [];
  let showCursor = 20;
  let showToast = false;
  let toastSuccess = true;
  let toastText = '';

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.comfyApp;

    files = await fetchFiles('files', comfyUrl);

    window.addEventListener('scroll', () => { showCursor = onScroll(showCursor, files.length); });
  });

  async function onClickLoad(file: any) {
    const res = await fetch(file.url);
    const blob = await res.blob();
    const fileObj = new File([blob], file.name, {
      type: res.headers.get('Content-Type') || '',
    });
    await comfyApp.handleFile(fileObj);
  }

  async function onCollect(file: any) {
    const res = await fetch(comfyUrl + '/browser/collections', {
      method: 'POST',
      body: JSON.stringify({
        filename: file.name,
        folder_path: file.folder_path,
      }),
    });

    toastSuccess = res.ok;
    if (toastSuccess) {
      toastText = 'Added to collections';
    } else {
      toastText = 'Failed to add to collections. Please check the ComfyUI server.';
    }
    showToast = true;
    setTimeout(() => showToast = false, 2000);
  }

  async function onDelete(file: any) {
    const ret = confirm('You will delete this file? ' + file.name);
    if (!ret) {
      return;
    }

    const res = await fetch(comfyUrl + '/browser/files', {
      method: 'DELETE',
      body: JSON.stringify({
        type: 'files',
        filename: file.name,
        folder_path: file.folder_path,
      }),
    });

    toastSuccess = res.ok;
    if (toastSuccess) {
      toastText = 'Deleted the file ' + file.name;
    } else {
      toastText = 'Failed to delete the file. Please check the ComfyUI server.';
    }
    showToast = true;
    setTimeout(() => showToast = false, 2000);
    files = files.filter(f => f != file);
  }
</script>

<div class="grid grid-cols-4 lg:grid-cols-6 gap-2 bg-base-300">
  {#each files.slice(0, showCursor) as file}
    {#if ['image', 'video'].includes(file.fileType)}
      <div class="bg-base-100">
        <div class="flex items-center">
          <MediaShow {file} styleClass="w-full h-36" />
        </div>

        <p class="font-bold max-h-12 leading-6 .no-scrollbar overflow-auto">{file.name}</p>
        <p class="text-gray-500">{file.formattedDatetime}</p>
        <p class="text-gray-500">{file.formattedSize}</p>

        <div class="">
          {#if comfyApp}
            <button
              class="btn btn-link btn-sm p-0 no-underline text-accent"
              on:click={async () => await onClickLoad(file)}
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

<Toast {showToast} {toastSuccess} {toastText} />
