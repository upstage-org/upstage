<template>
  <div :title="'Joined ' + joinedAt.fromNow()" @click="tagPlayer">
    <span class="icon">
      <i
        class="fas"
        :class="{
          'fa-user': session.isPlayer,
          'fa-desktop': !session.isPlayer,
          'has-text-success': isOnline,
        }"
      ></i>
    </span>
    {{ session.nickname }}
  </div>
</template>

<script>
import { computed } from "@vue/runtime-core";
import moment from "moment";
import { useStore } from "vuex";
export default {
  props: ["session"],
  setup: (props) => {
    const store = useStore();
    const joinedAt = computed(() => {
      return moment(new Date(props.session.at));
    });
    const isOnline = computed(() => {
      return moment().diff(joinedAt.value, "minutes") < 60;
    });

    const tagPlayer = () => {
      if (props.session.isPlayer) {
        store.commit('stage/TAG_PLAYER', props.session)
        store.dispatch("stage/showPlayerChat", true);
      }
    };
    return { joinedAt, isOnline, tagPlayer };
  },
};
</script>

<style scoped>
div {
  text-align: left;
}
</style>