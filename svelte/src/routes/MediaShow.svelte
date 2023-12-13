<script lang="ts">
  export let file: any;
  export let styleClass: string;
  export let onClickDir: Function;
</script>


<div class={styleClass}>
  {#if file.type === 'dir'}
    <button
      class="w-full h-full flex items-center justify-center"
      on:click={() => onClickDir(file)}
    >
      <span class="font-bold text-xl">
        Folder
      </span>
    </button>
  {:else}
    <a
      href={file.url}
      target="_blank"
      style="height: inherit; width: inherit;"
    >
      {#if file.fileType === 'json'}
        <div class="w-full h-full flex items-center justify-center">
          <span class="font-bold text-xl">
            JSON
          </span>
        </div>
      {/if}
      {#if file.fileType === 'image'}
        <img
          class="h-full w-full object-contain"
          loading="lazy"
          src={file.url}
          alt={file.name} />
      {/if}
      {#if file.fileType === 'video'}
        <video
          class="h-full w-full object-contain pb-0.5 border-0.5 border-black"
          src={file.url}
          loop={true}
          autoplay={true}
          muted={true}
        >
          <track kind="captions" />
        </video>
      {/if}
    </a>
  {/if}
</div>
