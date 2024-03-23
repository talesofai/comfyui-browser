<script lang="ts">
  import type { ImgResult } from './models';
  import { TableMode, comfyUrl, imageWidth, mode } from './store';
  import { db, getScore, getUser, updateScore, type User } from '$lib/db';
  export let value: ImgResult;
  export let width = 100;
  import { createRefetchStatisticPublisher } from './store';
  let refetch = createRefetchStatisticPublisher();
  let api = '';
  comfyUrl.subscribe((d) => (api = d));

  let like = false;
  let _mode = TableMode.View;
  imageWidth.subscribe((d) => {
    width = d;
  });

  mode.subscribe((v) => {
    _mode = v;
    if (v === TableMode.Score && value.uuid)
      db.scoreboard
        .where('uuid')
        .equals(value.uuid)
        .toArray()
        .then((arr) => {
          if (arr.length > 0 && arr[0].score > 0) {
            like = true;
          } else {
            like = false;
          }
        });
  });

  function updateSelfScore(score: number) {
    return updateScore(value.uuid, { score });
  }

  async function onLike() {
    const { score } = (await getScore(value.uuid)) ?? {};
    if (score === undefined) {
      await db.scoreboard.add({
        uuid: value.uuid,
        score: 1,
        link: value.src,
        ctime: Date.now(),
        mtime: Date.now(),
      });
    } else if (score === 1) {
      return;
    } else {
      await updateSelfScore(1);
    }
    return apiUpdateScore(1)
      .then(async (res) => {
        if (res && res.ok) {
          like = true;
          refetch();
        } else await updateSelfScore(0);
      })
      .catch(() => {
        updateSelfScore(0);
      });
  }

  async function onDislike() {
    const { score } = (await getScore(value.uuid)) ?? {};
    if (score === undefined || score === 0) {
      return;
    }
    await updateSelfScore(0);
    return apiUpdateScore(0)
      .then(async (res) => {
        if (res && res.ok) {
          like = false;
          refetch();
        } else await updateSelfScore(1);
      })
      .catch(() => {
        updateSelfScore(1);
      });
  }

  async function apiUpdateScore(score: number) {
    const user = await getUser();
    if (!user) return;
    return fetch(api + '/browser/xyz_plot/score', {
      method: 'PUT',
      body: JSON.stringify({
        user: user.name,
        source: value.uuid,
        score,
      }),
    });
  }
</script>

<div class="px-0.5 box-border inline-block relative" style={`width:${width}px`}>
  <a href={value.src} target="_blank">
    <img
      class="w-full"
      src={value.src}
      alt={value.uuid}
      style={`width:${width}px`}
    />
  </a>
  {#if _mode === TableMode.Score}
    <button
      class="absolute w-full h-full top-0 left-0 flex justify-end items-end p-1"
      tabindex="0"
      on:click={like ? onDislike : onLike}
    >
      <svg class="inline-block w-1/4" viewBox="0 0 1024 1024">
        <path
          d="M725.333333 192c-89.6 0-168.533333 44.8-213.333333 115.2C467.2 236.8 388.266667 192 298.666667 192 157.866667 192 42.666667 307.2 42.666667 448c0 253.866667 469.333333 512 469.333333 512s469.333333-256 469.333333-512c0-140.8-115.2-256-256-256z"
          fill={like ? '#F44336' : 'grey'}
        />
      </svg>
    </button>
  {/if}
</div>
