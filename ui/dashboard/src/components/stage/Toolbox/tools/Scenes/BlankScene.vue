<template>
  <div @click="createScene" class="is-pulled-left">
    <div class="icon is-large">
      <Icon src="new.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Blank Scene</span>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
import { useStore } from "vuex";
export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const createScene = async () => {
      if (
        confirm(
          "Create a new blank scene will erase everything on the stage. Make sure your scene is saved before you do this. Are you sure you want to continue?"
        )
      ) {
        store.dispatch("stage/blankScene");
      }
    };
    return { createScene };
  },
};
</script>

<style>
</style>