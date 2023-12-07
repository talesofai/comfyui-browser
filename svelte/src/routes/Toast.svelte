<script>
  export let showToast = false;
  export let toastSuccess = true;
  export let toastText = '';
</script>

{#if showToast}
  <div class="toast toast-center" >
    <div class="alert alert-{toastSuccess ? 'success' : 'error'}">
      <span>{toastText}</span>
    </div>
  </div>
{/if}
