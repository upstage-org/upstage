<template>
  <router-link :to="`/${stage.fileLocation}`" class="stage">
    <img class="cover" :src="coverImage(stage.cover)" lazy />
    <PlayerAudienceCounter :stage-url="stage.fileLocation" class="counter" />
    <span class="name">{{ stage.name }}</span>
  </router-link>
</template>

<script setup>
import { defineProps } from "vue";
import PlayerAudienceCounter from "components/stage/PlayerAudienceCounter.vue";
import { absolutePath } from "utils/common";

const props = defineProps({
  stage: {
    type: Object,
    required: true,
  },
  fallbackCover: {
    type: String,
  },
});
console.log(
  props.fallbackCover,
  `/img/${props.fallbackCover}`,
);
const coverImage = (src) =>
  src ? absolutePath(src) : `/img/${props.fallbackCover}`;
</script>

<style lang="scss" scoped>
.stage {
  color: black;
  text-shadow: -3px 0 #007011;
  position: relative;
  font-weight: bold;
  font-size: 25px;
  border: 1px solid black;
  border-top: 10px solid #007011;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  box-shadow: 10px 5px 0 0 black;
  color: white;
  border-radius: 12px;
  overflow: hidden;

  .cover {
    width: 100%;
    height: 100%;
    min-height: 200px;
    background-size: cover;
  }

  .name {
    position: absolute;
    z-index: 10;
    padding: 2rem;
  }

  .counter {
    position: absolute;
    right: 10px;
    top: 10px;
    width: auto !important;
  }
}
</style>
