<script lang="ts">
  export let activeTab = 'outputs';

  $: activeTabClass = function(tab: string) {
    return tab === activeTab ? 'tab-active' : '';
  }

  async function onClickTab(tab: string) {
    let url = new URL(window.location.href);
    url.searchParams.delete('folder_path');
    url.searchParams.set('tab', tab);
    window.location.href = url.toString();
    //activeTab = tab;
  }
</script>

<div role="tablist" class="tabs tabs-boxed sticky top-0">
  <button
    role="tab"
    class="tab {activeTabClass('outputs')}"
    on:click={() => onClickTab('outputs')}
  >
    Outputs
  </button>
  <button
    role="tab"
    class="tab {activeTabClass('collections')}"
    on:click={() => onClickTab('collections')}
  >
    Collections
  </button>
</div>
