<script lang="ts">
  import type { Axis, AxisScore } from './models';
  import Score from './score.svelte';
  import TableHolder from './table-holder.svelte';
  export let value: Axis;
  export let score: AxisScore | undefined;
</script>

<div class="border box-border inline-block">
  <div class="text-center font-bold">
    {#if score}
      <Score score={score.score} />
    {/if}
    {value.value}
  </div>
  <div class="flex justify-around">
    {#each value.children as item}
      <TableHolder value={item} {score} />
    {/each}
  </div>
</div>
