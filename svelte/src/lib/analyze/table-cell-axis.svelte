<script lang="ts">
  import type { Axis } from '../../routes/analyze/models';
  import TableHolder from './table-holder.svelte';
  export let value: Axis;
</script>

<div class="m-1 border">
  <div class="text-center font-bold">
    {value.value}
  </div>
  <div class="flex justify-around my-1">
    {#each value.children as item}
      <TableHolder value={item} />
    {/each}
  </div>
</div>
