<template>
  <a-layout-footer
    class="text-sm opacity-50 p-0 flex justify-center items-center"
  >
    UpStage v{{ version }}&nbsp;-&nbsp;
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
