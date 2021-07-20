<template>
  <footer class="footer">
    <div class="content has-text-centered">
      UpStage v4 -
      <span v-if="release">{{ release }}</span>
      <span v-else>Under construction</span>
    </div>
  </footer>
</template>

<script>
import { versionAlias } from "../../package.json";

export default {
  setup: () => {
    return { release: versionAlias };
  },
};
</script>

<style>
footer.footer {
  clear: both;
  position: relative;
  padding: 1rem;
}
</style>