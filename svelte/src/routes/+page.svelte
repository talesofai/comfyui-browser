<script lang="ts">
  import { onMount } from "svelte";
  import dayjs from 'dayjs';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let files: Array<any> = [];

  onMount(async () => {
    const res = await fetch(comfyUrl + '/browser/files');
    const ret = await res.json();

    files = ret.files;
    files.forEach(f => {
      const extname = f.name.split('.').pop().toLowerCase();
      f['fileType'] = 'unknown';
      if (['png', 'webp', 'jpeg', 'jpg', 'gif'].includes(extname)) {
        f['fileType'] = 'image';
      }
      if (['mp4', 'webm'].includes(extname)) {
        f['fileType'] = 'video';
      }

      f['url'] = `${comfyUrl}/view?filename=${f.name}`;

      const d = dayjs.unix(f.created_at);
      f['formattedDatetime'] = d.format('YYYY-MM-DD HH-mm-ss');

      if (f['bytes'] / 1024 / 1024 > 1) {
        f['formattedSize'] = (f['bytes'] / 1024 / 1024).toFixed(2) + ' MB';
      } else {
        f['formattedSize'] = Math.round(f['bytes'] / 1024) + ' KB';
      }
    });
  });
</script>

<div class="grid grid-cols-4 lg:grid-cols-6 gap-2">
  {#each files as file}
    {#if ['image', 'video'].includes(file.fileType) }
      <div class="browser-item">
        <div class="flex items-center">
          {#if file.fileType === 'image' }
            <img
              class=""
              src={file.url}
              alt={file.name} />
          {/if}
          {#if file.fileType === 'video' }
            <video
              class="object-contain pb-0.5 border-0.5 border-black"
              src={file.url}
              loop={true}
              autoplay={true}
              muted={true}
            >
              <track kind="captions" />
            </video>
          {/if}
        </div>

        <p>{file.name}</p>
        <p>{file.formattedDatetime}</p>
        <p>{file.formattedSize}</p>
      </div>
    {/if}
  {/each}
</div>

<style lang="postcss">
  .browser-item {
    @apply border-2;
  }

</style>
