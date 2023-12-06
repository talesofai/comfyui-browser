<script lang="ts">
  import { onMount } from "svelte";

  export let comfyApp: any;
  export let files: Array<any> = [];
  let showCursor = 20;

  onMount(() => {
    window.addEventListener('scroll', onScroll);
  });

  async function onClickLoad(file: any) {
    const res = await fetch(file.url);
    const blob = await res.blob();
    const fileObj = new File([blob], file.name, {
      type: res.headers.get('Content-Type') || '',
    });
    await comfyApp.handleFile(fileObj);
  }

  function onScroll() {
    if (showCursor >= files.length) {
      return;
    }

    const documentHeight = document.documentElement.scrollHeight;
    const scrollPosition = window.innerHeight + window.scrollY;
    if (scrollPosition >= documentHeight) {
      showCursor += 10;
    }
  }
</script>

<div
  class="grid grid-cols-4 lg:grid-cols-6 gap-2">
  {#each files.slice(0, showCursor) as file}
    {#if ['image', 'video'].includes(file.fileType)}
      <div class="browser-item">
        <a href={file.url} target="_blank">
          <div class="flex items-center">
            {#if file.fileType === 'image'}
              <img
                class=""
                src={file.url}
                alt={file.name} />
            {/if}
            {#if file.fileType === 'video'}
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
        </a>

        <p>{file.name}</p>
        <p>{file.formattedDatetime}</p>
        <p>{file.formattedSize}</p>

        {#if comfyApp}
          <button
            class="btn btn-ghost"
            on:click={async () => await onClickLoad(file)}
          >Load</button>
        {/if}
      </div>
    {/if}
  {/each}
</div>

<style lang="postcss">
  .browser-item {
    @apply border-2;
  }
</style>
