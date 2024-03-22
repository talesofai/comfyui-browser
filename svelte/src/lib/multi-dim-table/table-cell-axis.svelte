<script lang="ts">
  import type { Axis, AxisScore } from './models';
  import Score from './score.svelte';
  import TableHolder from './table-holder.svelte';
  export let value: Axis;
  export let score: AxisScore | undefined;
</script>

<div class="m-1 border box-border inline-block">
  <div class="text-center font-bold">
    {value.value}
    {#if score}
      <Score score={score.score} />
    {/if}
  </div>
  <div class="flex justify-around my-1">
    {#each value.children as item}
      <TableHolder value={item} {score} />
    {/each}
  </div>
</div>
