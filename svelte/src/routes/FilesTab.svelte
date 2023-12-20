<script lang="ts">
  import Toast from './Toast.svelte';
  import FilesList from './FilesList.svelte';

  export let comfyUrl: string;

  let toast: Toast;
</script>

<FilesList folderType="outputs" {comfyUrl} {toast} />

<Toast bind:this={toast} />
