<script lang="ts">
  import { onMount } from "svelte";
  import { fetchFiles, onScroll } from './utils';
  import MediaShow from "./MediaShow.svelte";

  export let comfyUrl: string;

  let comfyApp: any;
  let files: Array<any> = [];
  let showCursor = 20;

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.comfyApp || comfyUrl; //comfyUrl is for local debug

    files = await fetchFiles('collections', comfyUrl);

    window.addEventListener('scroll', () => { showCursor = onScroll(showCursor, files.length); });
  });


</script>


<div>
  {#each files.slice(0, showCursor) as file}
    <div>
      <MediaShow {file} />
    </div>
  {/each}
</div>
