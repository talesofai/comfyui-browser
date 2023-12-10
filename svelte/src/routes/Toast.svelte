<script lang="ts">
  export let showToast = false;
  export let toastSuccess = true;
  export let toastText = '';

  export function show(
    isSuccess: boolean,
    successText: string,
    failText: string,
    duration = 2000
  ) {
    toastSuccess = isSuccess;
    toastText = isSuccess ? successText : failText;
    showToast = true;
    setTimeout(() => showToast = false, duration);
  }
</script>

{#if showToast}
  <div class="toast toast-center" >
    <div class="alert {toastSuccess ? 'alert-success' : 'alert-error'}">
      <span>{toastText}</span>
    </div>
  </div>
{/if}
