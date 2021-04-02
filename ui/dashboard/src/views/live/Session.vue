<template>
  <div :title="'Joined ' + joinedAt.fromNow()">
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
export default {
  props: ["session"],
  setup: (props) => {
    const joinedAt = computed(() => {
      return moment(new Date(props.session.at));
    });
    const isOnline = computed(() => {
      return moment().diff(joinedAt.value, "minutes") < 60;
    });
    return { joinedAt, isOnline };
  },
};
</script>

<style>
</style>