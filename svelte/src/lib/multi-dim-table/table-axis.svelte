<script lang="ts">
  import Score from './score.svelte';
  import type { Axis, AxisScore } from './models';
  import TableHolder from './table-holder.svelte';
  import { el } from '@faker-js/faker';
  import { zip } from './utils';
  export let axis: Axis;
  export let score: AxisScore | undefined;
</script>

<tr>
  <!-- prompts -->
  <th style="max-width:30vw" class="z-10">
    {axis.value}
    {#if score}
      <Score score={score.score} />
    {/if}
  </th>
  {#if score && score.children}
    {#each zip(axis.children, score.children) as [dim2, score2]}
      {#if dim2.type === 'axis' && score2.children}
        <td>
          {#each zip(dim2.children, score2.children) as [dim3, score3]}
            <TableHolder value={dim3} score={score3}></TableHolder>
          {/each}
        </td>
      {/if}
    {/each}
  {:else}
    {#each axis.children as dim2}
      {#if dim2.type === 'axis'}
        <td>
          {#each dim2.children as dim3}
            <TableHolder value={dim3} score={undefined}></TableHolder>
          {/each}
        </td>
      {/if}
    {/each}
  {/if}
</tr>
