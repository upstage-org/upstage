<template>
  <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
    <div class="column has-text-centered has-text-light">
      <i class="fas fa-comments fa-4x"></i>
      <p class="subtitle has-text-light">No messages yet!</p>
    </div>
  </div>
  <div v-else>
    <p v-for="item in messages" :key="item">
      <small>
        <b>{{ item.user }}: </b>
      </small>
      <span
        class="tag message"
        :style="
          'background-color: ' + item.backgroundColor + '; color: ' + item.color
        "
        :data-tooltip="time(item.at)"
        >{{ item.message }}
      </span>
    </p>
  </div>
</template>

<script>
import moment from "moment";
export default {
  props: ["messages"],
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