<template>
  <Object :object="object" @hold="setAsPrimaryAvatar">
    <template #menu="slotProps">
      <MenuContent
        :object="object"
        :closeMenu="slotProps.closeMenu"
        v-model:active="active"
        @hold="setAsPrimaryAvatar"
      />
    </template>
  </Object>
</template>

<script>
import { computed, provide } from "@vue/runtime-core";
import Object from "../Object.vue";
import MenuContent from "./ContextMenu";
import { useStore } from "vuex";

export default {
  props: ["object"],
  components: { Object, MenuContent },
  setup: (props) => {
    const store = useStore();
    const loggedIn = computed(() => store.getters["auth/loggedIn"]);
    const holder = computed(() =>
      store.state.stage.sessions.find((s) => s.avatarId === props.object.id)
    );
    provide("holder", holder);

    const setAsPrimaryAvatar = () => {
      if (loggedIn.value && !holder.value && props.object.type !== "prop") {
        store
          .dispatch("user/setAvatarId", props.object.id)
          .then(props.closeMenu);
      }
    };

    return { setAsPrimaryAvatar, holder };
  },
};
</script>

<style>
</style>