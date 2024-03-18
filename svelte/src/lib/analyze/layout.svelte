<script lang="ts">
  export let extraItems:
    | undefined
    | {
        label: string;
        onClick?: () => void;
      }[] = undefined;

  export let sidebarItems: typeof extraItems = undefined;
</script>

<div class="drawer absolute h-full w-full overflow-y-hidden">
  <input id="my-drawer-3" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col">
    <!-- Navbar -->
    <div class="w-full navbar bg-base-300">
      <div class="flex-none">
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
      </div>
      <div class="flex-1 px-2 mx-2">
        <slot name="title" />
      </div>
      <div class="flex-none">
        {#if extraItems}
          <ul class="menu menu-horizontal items-center">
            <slot name="extra" />
            {#each extraItems as item}
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
