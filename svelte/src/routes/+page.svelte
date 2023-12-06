<script lang="ts">
  import dayjs from 'dayjs';
  import { onMount } from "svelte";

  import Tabs from './Tabs.svelte';
  import FilesList from "./FilesList.svelte";
  import CollectionsList from './CollectionsList.svelte';

  // @type {import('./$types').PageData}
  export let data: any;
  const { comfyUrl } = data;

  let activeTab = 'outputs';
  let comfyApp: any;
  let files: Array<any> = [];

  onMount(async () => {
    //@ts-ignore
    comfyApp = window.top.comfyApp || comfyUrl; //comfyUrl is for local debug

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

  function fetchFiles(type: 'files' | 'collections') {
  }
</script>

<Tabs bind:activeTab={activeTab} />

{#if activeTab === 'collections'}
  <CollectionsList />
{:else}
  <FilesList
    {files}
    {comfyApp}
  />
{/if}
