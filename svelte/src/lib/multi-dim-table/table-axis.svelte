<script lang="ts">
  import type { Axis } from './models';
  import TableHolder from './table-holder.svelte';
  export let axis: Axis;
</script>

<tr>
  <!-- prompts -->
  <th style="max-width:30vw" class="z-10">{axis.value}</th>
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
