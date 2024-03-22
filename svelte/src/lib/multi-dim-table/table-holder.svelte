<script lang="ts">
  import type { AxisScore, AxisValue } from './models';
  import TableCellAxis from './table-cell-axis.svelte';
  import TableCellImg from './table-cell-img.svelte';

  export let value: AxisValue;
  export let score: AxisScore | undefined;
</script>

{#if value.type === 'img'}
  <TableCellImg {value} />
{:else if value.type === 'axis'}
  <TableCellAxis {value} bind:score />
{/if}
