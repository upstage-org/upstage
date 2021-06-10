<template>
  <modal>
    <template #trigger>
      <Asset
        class="clickable"
        v-if="modelValue"
        :asset="{
          fileLocation: modelValue,
        }"
      />
      <button v-else class="button">Choose an image</button>
    </template>
    <template #header> Choose an existing image or upload new </template>
    <template #content="{ closeModal }">
      <div class="columns is-multiline">
        <div class="colum px-3 pt-1">
          <MediaUpload />
        </div>
      </div>
      <Skeleton v-if="loading" />
      <div v-else class="columns is-multiline">
        <div class="column is-3" v-for="item in mediaList" :key="item">
          <div class="card-image clickable" @click="select(item, closeModal)">
            <Asset :asset="item" />
          </div>
        </div>
      </div>
    </template>
  </modal>
</template>

<script>
import Modal from "@/components/Modal";
import Skeleton from "@/components/Skeleton";
import Asset from "@/components/Asset";
import { stageGraph } from "@/services/graphql";
import { useQuery } from "@/services/graphql/composable";
import MediaUpload from "@/views/backstage/Media/MediaUpload";
import { provide } from "@vue/runtime-core";
export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { Modal, Skeleton, Asset, MediaUpload },
  setup: (props, { emit }) => {
    const {
      loading,
      nodes: mediaList,
      refresh,
    } = useQuery(stageGraph.mediaList);
    provide("refresh", refresh);

    const select = (item, closeModal) => {
      emit("update:modelValue", item.fileLocation);
      closeModal();
    };

    return { loading, mediaList, select };
  },
};
</script>

<style>
</style>