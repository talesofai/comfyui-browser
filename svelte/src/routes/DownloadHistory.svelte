<script lang="ts">
  import dayjs from 'dayjs';
  import { onMount } from "svelte";
  import { formatFileSize } from './utils';

  export let comfyUrl: string;

  let downloads: Array<any> = [];

  onMount(async () => {
    const res = await fetch(comfyUrl + '/browser/downloads');
    const ret = await res.json();
    ret.download_logs.forEach((dl: any) => {
      let newDl = dl;
      const timeFormat = 'YYYY-MM-DD HH:mm:ss';
      newDl['formattedCreatedAt'] = dayjs.unix(dl.created_at).format(timeFormat);
      newDl['formattedUpdatedAt'] = dayjs.unix(dl.updated_at).format(timeFormat);
      newDl['percentStr'] = `${Math.floor(dl.downloaded_size/dl.total_size * 100)}%`;
      newDl['formattedDownloadedSize'] = formatFileSize(dl.downloaded_size);
      newDl['formattedTotalSize'] = formatFileSize(dl.total_size);

      downloads = [...downloads, newDl];
    });
  });
</script>

<ul class="space-y-2">
  {#each downloads as dl}
    <li class="bg-info-content">
      <p class="font-bold text-lg">{dl.filename}</p>
      <p class="text-gray-500 text-xs">
        <span>Created at: {dl.formattedCreatedAt}</span>
        <span>Updated at: {dl.formattedUpdatedAt}</span>
      </p>
      <p class="text-gray-500 text-xs">URL: {dl.download_url}</p>
      <p class="text-gray-500 text-xs">Save in: {dl.save_in}</p>
      {#if dl.total_size !== 0}
        <div>
          <span>{dl.formattedDownloadedSize}/{dl.formattedTotalSize}</span>
          <span>{dl.percentStr}</span>
          <progress
            class="progress progress-primary"
            value={dl.downloaded_size}
            max={dl.total_size} >
          </progress>
        </div>
      {:else}
        <p>Result: {dl.result}</p>
      {/if}
    </li>
  {/each}
</ul>
