<template>
  <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
    <div class="column has-text-centered has-text-light">
      <i class="fas fa-comments fa-4x"></i>
      <p class="subtitle has-text-light">No messages yet!</p>
    </div>
  </div>
  <div v-else>
    <p
      v-for="item in messages"
      :key="item"
      :style="{ opacity: item.isPlayer ? 1 : 0.5 }"
    >
      <small style="font-size: 1em">
        <b v-if="item.isPlayer">{{ item.user }}: </b>
        <span v-else>{{ item.user }}: </span>
      </small>
      <span
        class="tag message"
        :style="{
          'font-size': '1em',
        }"
        :class="messageClass[item.behavior]"
        :title="time(item.at)"
      >
        <Linkify>{{ item.message }}</Linkify>
      </span>
    </p>
  </div>
</template>

<script>
import moment from "moment";
import Linkify from "@/components/Linkify";
export default {
  props: ["messages", "style"],
  components: { Linkify },
  data: function () {
    return {
      messageClass: {
        think: "has-text-info has-background-info-light",
        shout: "has-text-danger",
      },
    };
  },
  methods: {
    time(value) {
      return moment(value).fromNow();
    },
  },
};
</script>

<style lang="scss">
.tag.message {
  white-space: break-spaces;
  height: unset;
}
</style>