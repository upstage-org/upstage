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
      <button v-else class="button">{{ $t("choose_an_image") }}</button>
    </template>
    <template #header>{{
      $t("choose_an_existing_image_or_upload_new")
    }}</template>
    <template #content="{ closeModal }">
      <div class="columns is-multiline">
        <div class="colum px-3 pt-1">
          <MediaUpload />
        </div>
      </div>
      <Loading v-if="loading" />
      <div v-else class="columns is-multiline">
        <div class="column is-12">
          <div class="columns">
            <div class="column panel-heading">
              <p class="control has-icons-left">
                <input
                  class="input"
                  type="text"
                  placeholder="Search Media"
                  v-model="filter.name"
                />
                <span class="icon is-left">
                  <i class="fas fa-search" aria-hidden="true"></i>
                </span>
              </p>
            </div>
            <Dropdown
              class="column"
              v-model="filter.mediaType"
              :data="types"
              :render-label="
                (type) => (type.name === 'media' ? 'All types' : type.name)
              "
              :render-value="(type) => type"
              style="width: 100%"
              fixed
              placeholder="All Types"
            />
            <Dropdown
              class="column"
              v-model="filter.owner"
              :data="users"
              :render-label="(user) => displayName(user)"
              :render-value="(user) => user"
              style="width: 100%"
              fixed
              placeholder="All Users"
            />
            <Dropdown
              class="column"
              v-model="filter.stage"
              :data="stages"
              :render-label="(stage) => stage.name"
              :render-value="(stage) => stage"
              style="width: 100%"
              fixed
              placeholder="All Stages"
            />
          </div>
        </div>
        <div class="column is-12 gallery">
          <div v-for="item in availableImages" :key="item">
            <div class="card-image clickable" @click="select(item, closeModal)">
              <Asset :asset="item" />
            </div>
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
import { computed, provide, reactive } from "@vue/runtime-core";
import Dropdown from "./Dropdown";
import { displayName } from "@/utils/auth";
export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { Modal, Loading, Asset, MediaUpload, Dropdown },
  setup: (props, { emit }) => {
    const {
      loading,
      nodes: mediaList,
      refresh,
    } = useQuery(stageGraph.mediaList);
    const type_dis = ["avatar", "prop", "backdrop", "shape", "curtain"];
    provide("refresh", refresh);

    const select = (item, closeModal) => {
      emit("update:modelValue", item.src);
      closeModal();
    };

    const filter = reactive({
      name: null,
      mediaType: null,
      owner: null,
      stage: null,
    });

    const { nodes: typesData } = useQuery(stageGraph.assetTypeList);
    const types = computed(() => {
      const list = [];
      list.push({ id: null, name: "All Types" });
      typesData.value
        .filter((m) => type_dis.includes(m.name))
        .forEach((type) => list.push(type));
      return list;
    });

    const users = computed(() => {
      let list = [];
      list.push({ id: null, displayName: "All Users" });
      if (mediaList.value) {
        mediaList.value.forEach(({ owner }) => {
          if (!list.some((user) => user.username === owner.username)) {
            list.push(owner);
          }
        });
      }
      return list;
    });

    const { nodes: stagesData } = useQuery(stageGraph.stageList);
    const stages = computed(() => {
      let list = [];
      list.push({ id: null, name: "All Stages" });
      if (stagesData.value) {
        stagesData.value.forEach((stage) => list.push(stage));
      }
      return list;
    });

    const availableImages = computed(() => {
      let list = mediaList.value;
      list = list.filter((m) => type_dis.includes(m.assetType.name));
      if (filter.name) {
        list = list.filter((media) =>
          media.name.toLowerCase().includes(filter.name.toLowerCase()),
        );
      }
      if (filter.mediaType && filter.mediaType.id) {
        list = list.filter(
          (media) => media.assetType.name === filter.mediaType.name,
        );
      }
      if (filter.owner && filter.owner.id) {
        list = list.filter(
          (media) => media.owner.username === filter.owner.username,
        );
      }
      if (filter.stage && filter.stage.id) {
        list = list.filter((media) =>
          media.stages.find((s) => s.id === filter.stage.dbId),
        );
      }
      return list;
    });

    return {
      loading,
      availableImages,
      select,
      filter,
      types,
      users,
      displayName,
      stages,
    };
  },
};
</script>

<style>
.dropdown .button {
  width: 95%;
}

.dropdown-content {
  margin-left: 1%;
}

.gallery {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-gap: 1.5rem;
}

.gallery .card-image {
  display: flex;
  justify-content: center;
}
.gallery img {
  height: 10vw;
  width: auto;
}
</style>
