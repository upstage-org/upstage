<template>
  <div @click="switchScene">
    <ContextMenu style="width: 100%; height: 100%; padding: 0">
      <template #trigger>
        <Skeleton :data="scene" nodrop>
          <div
            class="p-2 is-fullwidth is-flex is-flex-direction-column is-justify-content-space-between"
            :title="scene.name"
          >
            <Image :src="scene.scenePreview" style="height: auto; border-radius: 4px;" />
            <span class="tag mt-1 is-block">{{ scene.name }}</span>
          </div>
        </Skeleton>
      </template>
      <template #context>
        <a class="panel-block has-text-danger" @click="deleteScene">
          <span class="panel-icon">
            <Icon src="remove.svg" />
          </span>
          <span>Delete Scene</span>
        </a>
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
import Image from "@/components/Image";
import ContextMenu from "@/components/ContextMenu";
import { useStore } from "vuex";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import Skeleton from "../../Skeleton.vue";

export default {
  components: { Icon, Image, ContextMenu, Skeleton },
  props: ["scene"],
  setup: (props) => {
    const store = useStore();
    const switchScene = () => {
      store.dispatch("stage/switchScene", props.scene.id);
    };

    const { mutation } = useMutation(stageGraph.deleteScene, props.scene.id);
    const deleteScene = async () => {
      const result = await mutation();
      if (result.deleteScene) {
        const { message, success } = result.deleteScene;
        if (success) {
          notification.success(message);
          store.dispatch("stage/loadScenes");
        } else {
          notification.error(message);
        }
      }
    };

    return { switchScene, deleteScene };
  },
};
</script>

<style scoped>
.tag {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>