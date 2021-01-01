<template>
  <div id="chatbox" class="card is-light">
    <div class="card-content" ref="theContent">
      <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
        <div class="column has-text-centered has-text-light">
          <i class="fas fa-comments fa-4x"></i>
          <p class="title has-text-light">No messages yet!</p>
        </div>
      </div>
      <div v-else>
        <p v-for="item in messages" :key="item">
          <small>
            <time v-if="false">({{ item.at }}) </time>
            <b>{{ item.user }}: </b>
          </small>
          <span
            class="tag message"
            :style="
              'background-color: ' +
              item.backgroundColor +
              '; color: ' +
              item.color
            "
            >{{ item.message }}</span
          >
        </p>
      </div>
    </div>
    <footer class="card-footer">
      <div class="card-footer-item">
        <div class="control has-icons-right is-fullwidth">
          <input
            class="input is-rounded"
            placeholder="Type message"
            v-model="message"
            @keydown.enter="sendChat"
          />
          <button
            @click="sendChat"
            class="icon is-right clickable button is-primary is-rounded"
            :class="{ 'is-loading': loadingUser }"
            :disabled="loadingUser"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { computed, ref, watch } from "vue";
import anime from "animejs";
import { useStore } from "vuex";

export default {
  setup: () => {
    const theContent = ref();
    const store = useStore();

    const messages = computed(() => store.state.stage.chat.messages);
    const loadingUser = computed(() => store.state.user.loadingUser);
    const message = ref("");
    const scrollToEnd = () => {
      anime({
        targets: theContent.value,
        scrollTop: theContent.value?.scrollHeight,
        easing: "easeInOutQuad",
      });
    };
    const sendChat = () => {
      if (message.value.trim() && !loadingUser.value) {
        store.dispatch("stage/sendChat", message.value);
        message.value = "";
        scrollToEnd();
      }
    };
    watch(messages.value, scrollToEnd);

    return {
      messages,
      message,
      sendChat,
      theContent,
      loadingUser,
    };
  },
};
</script>

<style lang="scss" scoped>
#chatbox {
  position: fixed;
  width: 20%;
  min-width: 200px;
  height: calc(100vh - 135px);
  bottom: 16px;
  right: 16px;
  opacity: 0.9;

  .card-content {
    height: calc(100vh - 200px);
    overflow-y: auto;
  }
  .message {
    white-space: break-spaces;
    height: unset;
    color: white;
  }
}
</style>