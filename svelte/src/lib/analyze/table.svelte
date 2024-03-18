<script lang="ts">
  import type { Payload } from '../../routes/analyze/models';
  import TableAxis from './table-axis.svelte';
  export let height: number = 0;
  export let payload: Payload;
  console.log({ height });
</script>

<div class="overflow-x-auto w-full" style={`max-height: ${height}px`}>
  <table class="table table-xs table-pin-rows table-pin-cols table-zebra-grey">
    <thead>
      <tr>
        <th></th>
        {#each payload.result[0].children as r}
          {#if r.type === 'axis'}
            <td>{r.value}</td>
          {/if}
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each payload.result as axis}
        <TableAxis {axis} />
      {/each}
    </tbody>
  </table>
</div>
