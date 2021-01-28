<template>
  <div id="chatbox" class="card is-light" :class="{ collapsed }">
    <div class="actions">
      <button
        class="chat-setting button is-rounded is-light"
        @click="collapsed = !collapsed"
      >
        <span class="icon">
          <i
            class="fas"
            :class="{
              'fa-window-minimize': !collapsed,
              'fa-window-maximize': collapsed,
            }"
          ></i>
        </span>
      </button>
      <button
        class="chat-setting button is-rounded is-light"
        @click="openChatSetting"
      >
        <span class="icon">
          <i class="fas fa-cog"></i>
        </span>
      </button>
    </div>
    <div class="card-content" ref="theContent">
      <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
        <div class="column has-text-centered has-text-light">
          <i class="fas fa-comments fa-4x"></i>
          <p class="subtitle has-text-light">No messages yet!</p>
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
          <form autocomplete="off" @submit.prevent="sendChat">
            <emoji-input
              v-model="message"
              placeholder="Type message"
              :loading="loadingUser"
            />
          </form>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { computed, ref, watch } from "vue";
import anime from "animejs";
import { useStore } from "vuex";
import EmojiInput from "@/components/form/EmojiInput";

export default {
  components: { EmojiInput },
  setup: () => {
    const theContent = ref();
    const store = useStore();

    const messages = computed(() => store.state.stage.chat.messages);
    const loadingUser = computed(() => store.state.user.loadingUser);
    const message = ref("");
    const collapsed = ref(false);
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

    const openChatSetting = () =>
      store.dispatch("stage/openSettingPopup", {
        type: "Chat",
        title: "Change your nick name",
      });

    return {
      messages,
      message,
      sendChat,
      theContent,
      loadingUser,
      openChatSetting,
      collapsed,
    };
  },
};
</script>

<style lang="scss" scoped>
#chatbox {
  position: fixed;
  width: 20%;
  min-width: 200px;
  height: calc(100% - 135px);
  bottom: 16px;
  right: 16px;
  opacity: 0.9;
  overflow: visible;

  .card-content {
    height: calc(100% - 64px);
    overflow-y: auto;
    padding-top: 36px;
  }

  &.collapsed {
    height: 108px;
    .card-content {
      padding-top: 20px;
      height: 0;
      > div {
        display: none;
      }
    }
  }

  .message {
    white-space: break-spaces;
    height: unset;
    color: white;
  }
  .actions {
    position: absolute;
    right: 24px;
    top: 10px;
    button {
      width: 26px;
      height: 26px;
      padding: 0;
      margin-left: 6px;
    }
  }
  .control.has-icons-right .input {
    padding-right: 50px !important;
  }
}
</style>