<script lang="ts">
  import type { Axis } from '../../routes/analyze/models';
  import TableHolder from './table-holder.svelte';
  export let axis: Axis;
</script>

<tr>
  <!-- prompts -->
  <th>{axis.value}</th>
  {#each axis.children as dim2}
    {#if dim2.type === 'axis'}
      <td>
        {#each dim2.children as dim3}
          <TableHolder value={dim3}></TableHolder>
        {/each}
      </td>
    {/if}
  {/each}
</tr>
