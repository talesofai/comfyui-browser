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

    files = await fetchFiles('collections', comfyUrl);

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
    const ret = await updateFile(file, {
      filename: value,
      notes: file.notes || '',
      folder_path: file.folder_path,
    });

    toastSuccess = ret;
    if (toastSuccess) {
      toastText = 'Updated';
    } else {
      toastText = 'Failed to Update. Please check the ComfyUI server.';
    }
    showToast = true;
    setTimeout(() => showToast = false, 2000);
  }
  async function updateFileNotes(e: Event, file: any) {
    //@ts-ignore
    const value = e.target.value;
    const ret = await updateFile(file, {
      filename: file.name,
      notes: value,
      folder_path: file.folder_path,
    });

    toastSuccess = ret;
    if (toastSuccess) {
      toastText = 'Updated';
    } else {
      toastText = 'Failed to Update. Please check the ComfyUI server.';
    }
    showToast = true;
    setTimeout(() => showToast = false, 2000);
  }
</script>

<ul class="space-y-2">
  {#each files.slice(0, showCursor) as file}
    <li class="flex h-32 border-2">
      <MediaShow {file} styleClass="w-32 h-full flex justify-center items-center" />
      <div class="space-y-2">
        <input
          type="text"
          class="font-semibold"
          on:blur={(e) => updateFilename(e, file)}
          value={file.name}
        />
        <p class="text-gray-500">
          {file.formattedDatetime} | {file.formattedSize}
        </p>

        <button
          class="btn btn-ghost"
          on:click={async () => await onClickLoad(file)}
        >Load</button>
        <button
          class="btn btn-ghost"
          on:click={async () => await onDelete(file)}
        >Remove</button>
      </div>

      <div>
        <p>Notes:</p>
        <textarea
          name="notes"
          cols="30"
          rows="4"
          on:blur={(e) => updateFileNotes(e, file)}
        />
      </div>
    </li>
  {/each}
</ul>

<Toast {showToast} {toastSuccess} {toastText} />
