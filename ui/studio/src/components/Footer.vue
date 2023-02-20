<template>
  <a-layout-footer style="text-align: center">
    UpStage v{{ version }} -
    <span v-if="release">{{ release }}</span>
    <span v-else>{{ $t("under_construction") }}</span>
  </a-layout-footer>
</template>

<script>
import packageJson from "../../../dashboard/package.json";

export default {
  setup: () => {
    const { version, versionAlias } = packageJson;
    return { release: versionAlias, version };
  },
};
</script>
