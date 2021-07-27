<template>
  <modal>
    <template #trigger>
      <Asset
        class="clickable"
        v-if="modelValue"
        :asset="{
          src: modelValue,
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
      <Loading v-if="loading" />
      <div v-else class="columns is-multiline">
        <div class="column is-3" v-for="item in availableImages" :key="item">
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
import Loading from "@/components/Loading";
import Asset from "@/components/Asset";
import { stageGraph } from "@/services/graphql";
import { useQuery } from "@/services/graphql/composable";
import MediaUpload from "@/views/backstage/Media/MediaUpload";
import { computed, provide } from "@vue/runtime-core";
export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { Modal, Loading, Asset, MediaUpload },
  setup: (props, { emit }) => {
    const {
      loading,
      nodes: mediaList,
      refresh,
    } = useQuery(stageGraph.mediaList);
    const availableImages = computed(() =>
      mediaList.value.filter((m) =>
        ["avatar", "prop", "backdrop", "shape"].includes(m.assetType.name)
      )
    );
    provide("refresh", refresh);

    const select = (item, closeModal) => {
      emit("update:modelValue", item.src);
      closeModal();
    };

    return { loading, availableImages, select };
  },
};
</script>

<style>
</style>