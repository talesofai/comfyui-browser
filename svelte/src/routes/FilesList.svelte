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
    comfyApp = window.top.comfyApp || comfyUrl; //comfyUrl is for local debug

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

<div class="grid grid-cols-4 lg:grid-cols-6 gap-2">
  {#each files.slice(0, showCursor) as file}
    {#if ['image', 'video'].includes(file.fileType)}
      <div class="browser-item">
        <div class="flex items-center">
          <MediaShow {file} styleClass="" />
        </div>

        <p>{file.name}</p>
        <p>{file.formattedDatetime}</p>
        <p>{file.formattedSize}</p>

        {#if comfyApp}
          <button
            class="btn btn-ghost"
            on:click={async () => await onClickLoad(file)}
          >Load</button>
          <button
            class="btn btn-ghost"
            on:click={async () => await onCollect(file)}
          >Collect</button>
          <button
            class="btn btn-ghost"
            on:click={async () => await onDelete(file)}
          >Delete</button>
        {/if}
      </div>
    {/if}
  {/each}
</div>

<Toast {showToast} {toastSuccess} {toastText} />

<style lang="postcss">
  .browser-item {
    @apply border-2;
  }
</style>
