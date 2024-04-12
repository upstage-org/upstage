<template>
  <span class="text-xs whitespace-nowrap">
    UpStage v{{ version }} -
    <span v-if="release">{{ release }}</span>
    <span v-else>{{ $t("under_construction") }}</span>
  </span>
</template>

<script>
import packageJson from "../../package.json";

export default {
  setup: () => {
    const { version, versionAlias } = packageJson;
    return { release: versionAlias, version };
  },
};
</script>
