<script lang="ts" setup>
import { inject, ref } from "vue";
import { IframeSrc, SelectedMenu } from "symbols";
import MediaFilter from "components/media/MediaFilter.vue";
import MediaTable from "components/media/MediaTable.vue";
import MediaForm from "components/media/MediaForm/index.vue";
import StageFilter from "components/stage/StageFilter.vue";
import StageTable from "components/stage/StageTable.vue";

const selectedMenu = inject(SelectedMenu, ref(["stage"]));
const iframeSrc = inject<string>(IframeSrc);
const page = (name: string) => selectedMenu.value.includes(name);
</script>

<template>
  <template v-if="page('media')">
    <Dropzone>
      <MediaFilter />
      <MediaTable>
        <MediaForm />
      </MediaTable>
    </Dropzone>
  </template>
  <template v-else-if="page('stage')">
    <StageFilter />
    <StageTable v-show="!iframeSrc" />
  </template>
  <iframe v-if="iframeSrc" class="bg-gray-200" :src="iframeSrc" />
</template>

<style lang="less" scoped>
iframe {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  border: none;
}
</style>
