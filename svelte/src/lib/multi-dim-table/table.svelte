<script lang="ts">
  import { el } from '@faker-js/faker';
  import type { AxisScore, Payload } from './models';
  import Score from './score.svelte';
  import TableAxis from './table-axis.svelte';
  import { zip } from './utils';
  export let height: number = 0;
  export let payload: Payload;
  export let scores: AxisScore[] | undefined = undefined;

  let headScore: AxisScore[] | undefined = undefined;
  $: headScore = scores
    ? scores[0]
        .children!.map(
          (d) =>
            JSON.parse(
              JSON.stringify({ ...d, children: undefined }),
            ) as AxisScore,
        )
        .map((axis, idx) => ({
          ...axis,
          score:
            scores
              ?.map((axis) => axis.children![idx].score)
              .reduce((a, b) => a + b) ?? 0,
        }))
    : undefined;
</script>

<div
  class="overflow-x-auto max-w-full inline-block"
  style={`max-height: ${height}px`}
>
  <table class="table table-sm table-pin-rows table-pin-cols">
    <thead>
      <tr class="p-0">
        <th></th>
        {#if headScore}
          {#each zip(payload.result[0].children, headScore) as [axis, score]}
            {#if axis.type === 'axis'}
              <td class="p-0">
                <p class="max-h-16 text-wrap overflow-auto hover:overflow-y-scroll">
                  <Score score={score.score} />{axis.value}
                </p>
              </td>
            {/if}
          {/each}
        {:else}
          {#each payload.result[0].children as axis}
            {#if axis.type === 'axis'}
              <td class="p-0">
                <p class="max-h-12 text-wrap overflow-auto hover:overflow-y-scroll">{axis.value}</p>
              </td>
            {/if}
          {/each}
        {/if}
      </tr>
    </thead>
    <tbody>
      {#if scores}
        {#each zip(payload.result, scores) as [axis, score]}
          <TableAxis {axis} {score} />
        {/each}
      {:else}
        {#each payload.result as axis}
          <TableAxis {axis} score={undefined} />
        {/each}
      {/if}
    </tbody>
  </table>
</div>
