<template>
  <div class="card-content p-0">
    <a class="panel-block has-text-info" @click="setAsPrimaryAvatar">
      <span class="panel-icon">
        <i class="fas fa-map-marker-alt has-text-info"></i>
      </span>
      <span>Set as your avatar</span>
    </a>
    <a class="panel-block has-text-danger" @click="deleteObject">
      <span class="panel-icon">
        <i class="fas fa-trash has-text-danger"></i>
      </span>
      <span>Delete</span>
    </a>
    <a v-if="object.multi" class="panel-block has-text-danger">
      <div class="columns frame-selector is-multiline">
        <div
          v-for="frame in object.frames"
          :key="frame"
          class="column is-3"
          @click="switchFrame(frame)"
        >
          <Image :src="frame" />
        </div>
      </div>
    </a>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Image from "@/components/Image";

export default {
  props: ["object", "closeMenu"],
  components: { Image },
  setup: (props) => {
    const store = useStore();

    const setAsPrimaryAvatar = () => {
      const { name, id } = props.object;
      store.dispatch("user/setAvatarId", { id, name }).then(props.closeMenu);
    };

    const deleteObject = () => {
      store.dispatch("stage/deleteObject", props.object).then(props.closeMenu);
    };

    const switchFrame = (frame) => {
      store.dispatch("stage/switchFrame", {
        ...props.object,
        src: frame,
      });
    };

    return { switchFrame, setAsPrimaryAvatar, deleteObject };
  },
};
</script>

<style scoped lang="scss">
.frame-selector {
  width: 440px;

  @media screen and (max-width: 767px) {
    width: 100px;
    max-height: 50vh;
    overflow-y: auto;
  }
  .column {
    height: 100px;

    &:hover {
      background-color: hsl(0, 0%, 71%);
      cursor: pointer;
      border-radius: 5px;
    }
  }
}
</style>