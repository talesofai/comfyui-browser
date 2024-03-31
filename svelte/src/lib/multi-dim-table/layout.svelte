<script lang="ts">
  import { TableMode, imageWidth, mode } from './store';

  export let extraItems:
    | undefined
    | {
        label: string;
        onClick?: () => void;
      }[] = undefined;

  export let sidebarItems: typeof extraItems = undefined;

  let _imageWidth = 180;
  let _mode = TableMode.View;

  mode.subscribe((v) => {
    _mode = v;
  });
  $: {
    imageWidth.set(_imageWidth);
  }
</script>

<div class="drawer absolute h-full w-full overflow-y-hidden">
  <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col">
    <!-- Navbar -->
    <div class="w-full navbar p-0 bg-base-300 min-h-0">
      <div class="flex-none">
        {#if sidebarItems}
          <label
            for="my-drawer-3"
            aria-label="open sidebar"
            class="btn btn-square btn-ghost"
          >
            <svg
              fill="none"
              viewBox="0 0 24 24"
              class="inline-block w-6 h-6 stroke-current"
              ><path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </label>
        {/if}
      </div>
      <div class="flex-1 px-2 mx-2">
        <slot name="title" />
      </div>
      <div class="flex-none">
        {#if extraItems}
          <ul class="menu menu-horizontal items-center">
            <li>
              <div>
                <input
                  type="range"
                  min="50"
                  max="500"
                  bind:value={_imageWidth}
                  class="range"
                />
              </div>
            </li>

            <li>
              <button
                on:click={() => {
                  if (_mode === TableMode.Score) {
                    mode.set(TableMode.View);
                  } else {
                    mode.set(TableMode.Score);
                  }
                }}
              >
                {_mode === TableMode.Score ? 'Score Mode' : 'View Mode'}
              </button>
            </li>

            {#each extraItems as item}
              <li>
                <button on:click={item.onClick}>
                  {item.label}
                </button>
              </li>
            {/each}
          </ul>
        {/if}
      </div>
    </div>
    <slot />
  </div>
  <div class="drawer-side z-50">
    <label for="my-drawer-3" aria-label="close sidebar" class="drawer-overlay"
    ></label>
    {#if sidebarItems}
      <ul class="menu p-4 w-80 min-h-full bg-base-200">
        {#each sidebarItems as item}
          <li>
            <a on:click={item.onClick}>
              {item.label}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
