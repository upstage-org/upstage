<template>
  <div @click="switchScene">
    <ContextMenu style="width: 100%; height: 100%; padding: 0" prevent-clicking>
      <template #trigger>
        <Skeleton :data="scene" nodrop>
          <div
            class="p-2 is-fullwidth is-flex is-flex-direction-column is-justify-content-space-between"
            :title="scene.name"
          >
            <Image
              :src="scene.scenePreview"
              style="height: auto; border-radius: 4px"
            />
            <span class="tag mt-1 is-block">{{ scene.name }}</span>
          </div>
        </Skeleton>
      </template>
      <template #context>
        <a class="panel-block has-text-danger" @click="deleteScene">
          <span class="panel-icon">
            <Icon src="remove.svg" />
          </span>
          <span>{{ $t("delete_scene") }}</span>
        </a>
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import Icon from "components/Icon.vue";
import Image from "components/Image.vue";
import ContextMenu from "components/ContextMenu.vue";
import { useStore } from "vuex";
import { useMutation } from "services/graphql/composable";
import { stageGraph } from "services/graphql";
import { message } from "ant-design-vue";
import Skeleton from "../../Skeleton.vue";

export default {
  components: { Icon, Image, ContextMenu, Skeleton },
  props: ["scene"],
  setup: (props) => {
    const store = useStore();
    const switchScene = () => {
      store.dispatch("stage/switchScene", props.scene.id);
      const audios = JSON.parse(props.scene.payload).audios;
      const audioPlayers = JSON.parse(props.scene.payload).audioPlayers;
      audios.forEach((audio, index) => {
        audio.currentTime = audioPlayers[index].currentTime;
        audio.changed = true;
        audio.saken = true;
        store.dispatch("stage/updateAudioStatus", audio);
      });
    };

    const { mutation } = useMutation(stageGraph.deleteScene, props.scene.id);
    const deleteScene = async () => {
      const result = await mutation();
      if (result.deleteScene) {
        const { message, success } = result.deleteScene;
        if (success) {
          message.success(message);
          store.dispatch("stage/loadScenes");
        } else {
          message.error(message);
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
