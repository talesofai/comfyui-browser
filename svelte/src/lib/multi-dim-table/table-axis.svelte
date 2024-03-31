<script lang="ts">
  import Score from './score.svelte';
  import type { Axis, AxisScore } from './models';
  import TableHolder from './table-holder.svelte';
  import { zip } from './utils';
  export let axis: Axis;
  export let score: AxisScore | undefined;
</script>

<tr class="p-0 even:bg-stone-800 odd:bg-base-100">
  <!-- prompts -->
  <th class="z-10 p-0 max-w-44 bg-inherit">
    {#if score}
      <Score score={score.score} />
    {/if}
    {axis.value}
  </th>
  {#if score && score.children}
    {#each zip(axis.children, score.children) as [dim2, score2]}
      {#if dim2.type === 'axis' && score2.children}
        <td class="p-0">
          {#each zip(dim2.children, score2.children) as [dim3, score3]}
            <TableHolder value={dim3} score={score3}></TableHolder>
          {/each}
        </td>
      {/if}
    {/each}
  {:else}
    {#each axis.children as dim2}
      {#if dim2.type === 'axis'}
        <td class="p-0">
          {#each dim2.children as dim3}
            <TableHolder value={dim3} score={undefined}></TableHolder>
          {/each}
        </td>
      {/if}
    {/each}
  {/if}
</tr>
