<template>
  <span class="text-xs whitespace-nowrap">
    Studio v{{ version }} -
    <span v-if="release">{{ release }}</span>
    <span v-else>{{ $t("under_construction") }}</span>
  </span>
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
