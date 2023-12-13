<script lang="ts">
  import { onMount } from "svelte";
  import Toast from "./Toast.svelte";
  import FilesList from "./FilesList.svelte";

  export let comfyUrl: string;

  let sources: Array<any> = [];
  let toast: Toast;
  let selectedSource: any;

  onMount(async () => {
    const res = await fetch(comfyUrl + '/browser/sources');
    const ret = await res.json();
    sources = ret.sources;
    selectedSource = sources[0];
  });

  function onClickSource(source: any) {
    selectedSource = source;
  }
</script>

<div>
  <ul class="inline-block menu bg-base-200 w-56 p-0 [&_li>*]:rounded-none">
    {#each sources as source}
      <li>
        <button
          class="btn text-left"
          on:click={() => onClickSource(source)}
        >{source.name}</button>
      </li>
    {/each}
  </ul>

  <div class="inline-block w-auto">
    <FilesList
      folderType="sources"
      folderPath={selectedSource?.name}
      comfyUrl={comfyUrl}
      toast={toast}
    />
  </div>
</div>

<Toast bind:this={toast} />
