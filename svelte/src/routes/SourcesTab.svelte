<script lang="ts">
  import { onMount } from 'svelte';
  import { t } from 'svelte-i18n';
  import Toast from './Toast.svelte';
  import FilesList from './FilesList.svelte';

  export let comfyUrl: string;

  let sources: Array<any> = [];
  let toast: Toast;
  let sourceEditModal: any;
  let inputRepoUrl: string;
  let waitingForUrl: string = '';
  let folderPath = '';
  let allSources: Array<any> = [];
  let fileList: FilesList;
  let syncingSouce: any;

  $: tt = function(key: string) {
    return $t('sourcesTab.' + key);
  }

  async function refreshSources() {
    const res = await fetch(comfyUrl + '/browser/sources');
    const ret = await res.json();
    sources = ret.sources.map((s: any) => {
      s.homepage = '';
      if (s.url.startsWith('https://')) {
        s.homepage = s.url;
        if (s.homepage.endsWith('.git')) {
          s.homepage = s.homepage.slice(0, -4);
        }
      }

      return s;
    });
  }

  onMount(async () => {
    refreshSources();
    getAllSources();
  });

  function onClickSource(source: any) {
    folderPath = source.name;
  }

  async function onClickDeleteSource(source: any) {
    const ret = confirm(tt('You want to delete this source') + source.name);
    if (!ret) {
      return;
    }

    const res = await fetch(comfyUrl + `/browser/sources/${source.name}`, {
      method: 'DELETE',
    });

    if (res.ok) {
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      tt('Deleted this source'),
      tt('Failed to delete this source'),
    );
  }

  async function onClickSyncSource(source: any) {
    syncingSouce = source;
    const res = await fetch(comfyUrl + `/browser/sources/sync/${source.name}`, {
      method: 'POST',
    });
    syncingSouce = null;

    if (res.ok) {
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      'Synced ' + [source.author, source.name].join('/'),
      'Failed to sync this source. Please check the ComfyUI server.',
    );
  }

  function openEditModal() {
    sourceEditModal.showModal();
  }

  async function addSource(url: string) {
    if (!url) {
      toast.show(false, '', 'missing Git URL');
      return;
    }

    waitingForUrl = url;
    const res = await fetch(comfyUrl + '/browser/sources', {
      method: 'POST',
      body: JSON.stringify({
        repo_url: url,
      }),
    });
    waitingForUrl = '';

    if (res.ok) {
      refreshSources();
      fileList.refresh();
    }
    toast.show(
      res.ok,
      'Added a new source',
      'Failed to add a new source. Please check the ComfyUI server.',
    );
    sourceEditModal.close();
  }

  async function getAllSources() {
    const res = await fetch(comfyUrl + '/browser/sources/all');
    const ret = await res.json();
    allSources = ret.sources;
  }
</script>

<div class="drawer md:drawer-open">
  <input type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col pl-2">
    <FilesList
      folderType="sources"
      bind:folderPath
      {comfyUrl}
      {toast}
      bind:this={fileList}
    />
  </div>

  <div class="drawer-side border-r border-base-content pr-2">
    <ul class="menu bg-base-200 w-56 p-0 [&_li>*]:rounded-none">
      <li class="h-10">
        <button class="pl-2 btn-outline btn-accent" on:click={openEditModal}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            data-slot="icon"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
            />
          </svg>
          {tt('Add new source')}
        </button>
      </li>

      {#each sources as source}
        <li class="h-14">
          {#if source.homepage}
            <a
              class="h-14 px-0.5 flex items-center justify-center"
              href={source.homepage}
              target="_blank"
            >
              <!--TODO: using more general icon instead of GitHub-->
              <svg
                class="w-6 h-6 fill-accent"
                xmlns="http://www.w3.org/2000/svg"
                x="0px"
                y="0px"
                width="100"
                height="100"
                viewBox="0 0 30 30"
              >
                <path
                  d="M15,3C8.373,3,3,8.373,3,15c0,5.623,3.872,10.328,9.092,11.63C12.036,26.468,12,26.28,12,26.047v-2.051 c-0.487,0-1.303,0-1.508,0c-0.821,0-1.551-0.353-1.905-1.009c-0.393-0.729-0.461-1.844-1.435-2.526 c-0.289-0.227-0.069-0.486,0.264-0.451c0.615,0.174,1.125,0.596,1.605,1.222c0.478,0.627,0.703,0.769,1.596,0.769 c0.433,0,1.081-0.025,1.691-0.121c0.328-0.833,0.895-1.6,1.588-1.962c-3.996-0.411-5.903-2.399-5.903-5.098 c0-1.162,0.495-2.286,1.336-3.233C9.053,10.647,8.706,8.73,9.435,8c1.798,0,2.885,1.166,3.146,1.481C13.477,9.174,14.461,9,15.495,9 c1.036,0,2.024,0.174,2.922,0.483C18.675,9.17,19.763,8,21.565,8c0.732,0.731,0.381,2.656,0.102,3.594 c0.836,0.945,1.328,2.066,1.328,3.226c0,2.697-1.904,4.684-5.894,5.097C18.199,20.49,19,22.1,19,23.313v2.734 c0,0.104-0.023,0.179-0.035,0.268C23.641,24.676,27,20.236,27,15C27,8.373,21.627,3,15,3z"
                ></path>
              </svg>
            </a>
          {:else}
            <div class="h-14 px-0.5 flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                data-slot="icon"
                class="w-6 h-6 text-accent"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z"
                />
              </svg>
            </div>
          {/if}
          <button
            class="pl-2 h-14 line-clamp-2 overflow-hidden {source.name ==
            folderPath.split('/')[0]
              ? 'active'
              : ''}"
            on:click={() => onClickSource(source)}
            ><p class="w-40 truncate whitespace-normal">
              {source.name}
            </p></button
          >
          <button
            class="h-14 right-0 fixed flex items-center justify-center"
            on:click={() => onClickSyncSource(source)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="{syncingSouce == source ? 'text-accent' : ''} w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
              />
            </svg>
          </button>
        </li>
      {/each}
    </ul>
  </div>
</div>

<Toast bind:this={toast} />

<!-- Open the modal using ID.showModal() method -->
<dialog class="modal" bind:this={sourceEditModal}>
  <div class="modal-box w-5/6 max-w-5xl">
    <div class="mb-2 flex space-x-2">
      <input
        type="text"
        bind:value={inputRepoUrl}
        placeholder="https://github.com/comfyanonymous/ComfyUI_examples"
        class="grow input input-bordered"
      />
      <button
        class="btn btn-outline btn-primary"
        on:click={() => addSource(inputRepoUrl)}
        disabled={waitingForUrl.length > 0 || !inputRepoUrl}
        >{waitingForUrl === inputRepoUrl && inputRepoUrl
          ? tt('Subscribing...')
          : tt('Subscribe')}</button
      >
    </div>

    <div>
      {#if allSources.length === 0}
        <div class="w-full h-full flex items-center justify-center">
          <span class="font-bold text-4xl"> {$t('common.loading')} </span>
        </div>
      {/if}
      <ul class="space-y-1">
        {#each allSources as s}
          <li
            class="flex flex-nowrap space-x-2 h-20 border-b border-b-base-content"
          >
            <img src={`https://github.com/${s.author}.png`} alt={s.author} />
            <div class="w-80">
              <a class="link link-warning text-lg no-underline" href={s.url} target="_blank">
                <p class="line-clamp-2">{s.author}/{s.title}</p>
              </a>
              <a href={s.url} target="_blank">
                <img
                  src={`https://img.shields.io/github/stars${
                    new URL(s.url).pathname
                  }?style=flat-square`}
                  alt="stars"
                />
              </a>
            </div>
            <div class="w-72 grow overflow-auto">
              <p>{s.description}</p>
            </div>
            <div class="flex items-center justify-center">
              <button
                class="btn btn-outline btn-primary no-underline text-accent"
                on:click={() => addSource(s.url)}
                disabled={waitingForUrl.length > 0}
              >
                {waitingForUrl === s.url ? tt('Subscribing...') : tt('Subscribe')}
              </button>
            </div>
          </li>
        {/each}
      </ul>
    </div>
    <p class="mt-1 text-xs text-gray-500">
      You could open
      <a
        class="text-accent"
        target="_blank"
        href="https://github.com/talesofai/comfyui-browser/edit/main/data/sources.json"
      >
        a pull request
      </a>
      or submit
      <a
        class="text-accent"
        target="_blank"
        href="https://github.com/talesofai/comfyui-browser/issues/new?assignees=tzwm&labels=workflow-repo&projects=&template=new-workflow-repository.md&title=New+workflow+repo%3A"
      >
        an issue
      </a>
      to add your workflow repository here.<br />
      Thank you to everyone who contributes to the open community!
    </p>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
