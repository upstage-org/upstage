<template>
  <div
    id="chatbox"
    class="card is-light"
    :class="{ collapsed }"
    :style="{ opacity }"
  >
    <div class="actions">
      <Reaction v-if="collapsed" />
      <button
        class="chat-setting button is-rounded is-light"
        @click="collapsed = !collapsed"
      >
        <span class="icon">
          <Icon src="minimize.svg" size="32" class="mt-4" />
        </span>
      </button>
      <button
        class="chat-setting button is-rounded is-light"
        @click="openChatSetting"
      >
        <span class="icon">
          <Icon src="setting.svg" size="32" />
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
        <div v-if="!collapsed" class="is-fullwidth my-1" style="height: 30px">
          <Reaction :custom-emoji="true" />
        </div>
        <div class="control has-icons-right is-fullwidth">
          <emoji-input
            v-model="message"
            placeholder="Type message"
            :loading="loadingUser"
            @submit="sendChat"
          />
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
import Icon from "@/components/Icon";
import Reaction from "./Reaction";

export default {
  components: { EmojiInput, Reaction, Icon },
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
      });

    const opacity = computed(() => store.state.stage.chat.opacity);

    return {
      messages,
      message,
      sendChat,
      theContent,
      loadingUser,
      openChatSetting,
      collapsed,
      opacity,
    };
  },
};
</script>

<style lang="scss" scoped>
#chatbox {
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 20%;
  min-width: 250px;
  height: calc(100% - 135px);
  bottom: 16px;
  right: 16px;
  overflow: visible;
  z-index: 3;

  .card-content {
    flex-grow: 1;
    overflow-y: auto;
    padding-top: 36px;
  }
  .card-footer-item {
    flex-wrap: wrap;
    padding-top: 0;
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
    .card-footer-item {
      padding-top: 6px;
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