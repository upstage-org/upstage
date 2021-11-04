<script lang="ts" setup>
import { PropType, computed } from 'vue';
import { Media, MediaAttributes } from '../../models/studio';
import { absolutePath } from '../../utils/common';
const { media } = defineProps({
  media: {
    type: Object as PropType<Media>,
    required: true,
  }
})

console.log(media.description);
const attributes = computed<MediaAttributes>(() => {
  return JSON.parse(media.description || '{}');
})

</script>

<template>
  <audio v-if="media.assetType.name === 'audio'" controls class="w-48">
    <source :src="absolutePath(media.src)" />Your browser does not support the audio element.
  </audio>
  <video v-else-if="media.assetType.name === 'stream'" controls class="w-48">
    <source :src="absolutePath(media.src)" />Your browser does not support the video tag.
  </video>
  <a-carousel v-else-if="attributes.multi" arrows dots-class="slick-dots slick-thumb" class="w-48">
    <template #customPaging="props">
      <a>
        <img :src="absolutePath(attributes.frames[props.i])" />
      </a>
    </template>
    <div v-for="frame in attributes.frames" :key="frame">
      <a-image :src="absolutePath(frame)" />
    </div>
  </a-carousel>
  <a-image v-else :src="absolutePath(media.src)" class="w-24" />
</template>

<style scoped>
.ant-carousel :deep(.slick-dots) {
  position: relative;
  height: auto;
}
.ant-carousel :deep(.slick-slide img) {
  border: 5px solid #fff;
  display: block;
  margin: auto;
  max-width: 80%;
}
.ant-carousel :deep(.slick-arrow) {
  display: none !important;
}
.ant-carousel :deep(.slick-thumb) {
  bottom: 0px;
  display: flex;
}
.ant-carousel :deep(.slick-thumb li) {
  width: 45px;
}
.ant-carousel :deep(.slick-thumb li img) {
  width: 100%;
  height: 100%;
  transform: scale(0.8);
}
.ant-carousel :deep(.slick-thumb li.slick-active img) {
  transform: scale(1);
}
</style>