<template>
  <footer class="footer">
    <div class="content has-text-centered">
      UpStage v{{ version }} -
      <span v-if="release">{{ release }}</span>
      <span v-else>{{ $t("under_construction") }}</span>
    </div>
  </footer>
</template>

<script>
import { version, versionAlias } from "../../package.json";

export default {
  setup: () => {
    return { release: versionAlias, version };
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
