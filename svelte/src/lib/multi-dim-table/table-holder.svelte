<script lang="ts">
  import type { AxisValue } from './models';
  import TableCellAxis from './table-cell-axis.svelte';
  import TableCellImg from './table-cell-img.svelte';

  export let value: AxisValue;
</script>

{#if value.type === 'img'}
  <TableCellImg {value} />
{:else if value.type === 'axis'}
  <TableCellAxis {value} />
{/if}
