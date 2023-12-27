<script lang="ts">
  import Toast from "./Toast.svelte";

  export let comfyUrl: string;
  export let afterStartingDownload: Function;

  const modelTypes = [
    { text: 'Checkpoint', value: 'checkpoints' },
    { text: 'LoRA', value: 'loras' },
    { text: 'VAE', value: 'vae' },
    { text: 'Embedding', value: 'embeddings' },
    { text: 'ControlNet', value: 'controlnet' },
  ];

  let toast: Toast;
  let downloadUrl = '';
  let modelType = modelTypes[0].value;
  let filename = '';
  let overwrite = false;

  async function onClickDownload() {
    if (! downloadUrl) {
      toast.show(false, '', 'Invalid download URL');
      return;
    }

    const res = await fetch(comfyUrl + '/browser/downloads', {
      method: 'POST',
      body: JSON.stringify({
        download_url: downloadUrl,
        save_in: modelType,
        filename: filename,
        overwrite: overwrite,
      }),
    });

    toast.show(
      res.ok,
      'Download started',
      'Failed'
    );

    if (afterStartingDownload) {
      afterStartingDownload();
    }
  }
</script>

<div class="space-y-4">
  <div class="form-control w-full max-w-2xl">
    <div class="label">
      <span class="label-text">* Download URL</span>
    </div>
    <input
      type="text"
      placeholder="https://civitai.com/api/download/models/35516"
      class="input input-bordered w-full max-w-2xl"
      bind:value={downloadUrl}
    />
  </div>

  <div class="form-control w-full max-w-2xl">
    <div class="label">
      <span class="label-text">Filename(leave this blank if you want to auto detect this)</span>
    </div>
    <input
      type="text"
      class="input input-bordered w-full max-w-2xl"
      bind:value={filename}
    />
  </div>


  <div class="form-control w-full">
    <div class="label">
      <span class="label-text">* Select the modal type</span>
    </div>
    <select
      class="select select-bordered max-w-xs"
      bind:value={modelType}
    >
      {#each modelTypes as mt}
        <option value={mt.value}>{mt.text}</option>
      {/each}
    </select>
  </div>

  <div class="form-control w-full">
    <label class="cursor-pointer label max-w-xs">
      <span class="label-text">Overwrite the exist file?</span>
      <input type="checkbox" bind:checked={overwrite} class="checkbox checkbox-secondary" />
    </label>
  </div>

  <button
    class="btn btn-secondary btn-outline"
    on:click={onClickDownload}
  >
    Download
  </button>
</div>

<Toast bind:this={toast} />
