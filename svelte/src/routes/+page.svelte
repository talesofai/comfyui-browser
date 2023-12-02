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
  });
</script>

<p>
  { files }
</p>
