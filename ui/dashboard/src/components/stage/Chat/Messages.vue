<template>
  <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
    <div class="column has-text-centered has-text-light">
      <i class="fas fa-comments fa-4x"></i>
      <p class="subtitle has-text-light">No messages yet!</p>
    </div>
  </div>
  <div v-else>
    <p v-for="item in messages" :key="item">
      <small style="font-size: 1em">
        <b>{{ item.user }}: </b>
      </small>
      <span
        class="tag message"
        :style="
          'background-color: ' +
          item.backgroundColor +
          '; color: ' +
          item.color +
          '; font-size: .85714em'
        "
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
        shout: "has-background-danger has-text-white",
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