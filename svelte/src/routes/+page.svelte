<script lang="ts">
  import { onMount } from "svelte";

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let files: Array<any> = [];

  onMount(async () => {
    const res = await fetch(comfyUrl + '/browser/files');
    const ret = await res.json();

    files = ret.files;
    files.forEach(f => {
      f['extname'] = f.name.split('.').pop().toLowerCase();
      f['url'] = `${comfyUrl}/view?filename=${f.name}`;
    });
  });
</script>

<div class="grid grid-cols-6 gap-4">
  {#each files as file}
    {#if ['png', 'webp', 'jpeg', 'jpg', 'gif'].includes(file.extname) }
      <div>
        <img src={file.url} alt={file.name} />
      </div>
    {/if}
    {#if ['mp4, webm'].includes(file.extname) }
      <div>
        <video
          class="rounded-lg pb-0.5 border-0.5 border-black"
          src={file.url}
          loop={true}
          autoplay={true}
          muted={true}
        >
          <track kind="captions" />
        </video>
      </div>
    {/if}
  {/each}
</div>
