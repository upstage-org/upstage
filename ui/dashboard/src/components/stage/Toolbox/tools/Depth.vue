<template>
  <div v-for="object in objects" :key="object.id">
    <Icon
      class="current-avatar"
      v-if="object.holder"
      :style="{
        filter: `grayscale(${object.id === currentAvatar ? 0 : 1})`,
      }"
      src="my-avatar.svg"
    />
    <Skeleton :real="true" :data="object" />
  </div>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
import Skeleton from "../Skeleton";
import Icon from "@/components/Icon";

export default {
  components: { Skeleton, Icon },
  setup() {
    const store = useStore();
    const objects = computed(() => store.getters["stage/objects"]);
    const currentAvatar = computed(() => store.state.user.avatarId);

    return { objects, currentAvatar };
  },
};
</script>

<style lang="scss" scoped>
.current-avatar {
  position: absolute;
  z-index: 1;
  transform: translate(-50%, -65%);
}
</style>