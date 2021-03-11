<template>
  <div class="columns is-multiline">
    <div
      v-for="media in mediaList"
      :key="media"
      :class="`column media-column ${
        ['backdrop', 'audio'].includes(media.assetType.name) ? 'is-4' : 'is-2'
      }`"
    >
      <div class="">
        <span class="tag is-light is-small type-tag">
          {{ media.assetType.name }}
        </span>
        <div class="card-image">
          <Asset :asset="media" />
        </div>
        <header class="card-header">
          <p class="card-header-title">{{ media.name }}</p>
        </header>
      </div>
    </div>
  </div>
</template>

<script>
import { inject } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
import Asset from "@/components/Asset";

export default {
  components: { Asset },
  setup: () => {
    const mediaList = inject("mediaList");
    return { mediaList, absolutePath };
  },
};
</script>

<style>
.media-column {
  position: relative;
}
.type-tag {
  position: absolute;
  z-index: 10;
  top: 20px;
  right: 0;
}
</style>