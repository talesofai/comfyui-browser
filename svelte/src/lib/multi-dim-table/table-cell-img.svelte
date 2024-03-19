<script lang="ts">
  import type { ImgResult } from './models';
  import { imageWidth } from './store';
  export let value: ImgResult;
  export let width = 100;

  imageWidth.subscribe((d) => {
    width = d;
  });
</script>

<div class="px-0.5">
  <img style={`width:${width}px`} src={value.src} alt={value.uuid} />
</div>
