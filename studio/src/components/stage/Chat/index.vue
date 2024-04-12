<template>
  <transition :css="false" @enter="enter" @leave="leave">
    <div
      id="chatbox"
      :key="chatPosition"
      v-show="chatVisibility"
      class="card is-light"
      :class="{ collapsed, dark: chatDarkMode }"
      :style="{
        opacity,
        fontSize,
        width: `calc(20% + 3*${fontSize}`,
        height: `calc(100vh - ${stageSize.height}px - 64px)`,
        left: chatPosition === 'left' ? (canPlay ? '48px' : '16px') : 'unset',
      }"
    >
      <transition @enter="bounceUnread">
        <span
          v-if="collapsed && unreadMessages"
          :key="unreadMessages"
          :data-tooltip="`${unreadMessages} new message${
            unreadMessages > 1 ? 's' : ''
          }`"
          class="unread clickable tag is-danger is-small"
          @click="collapsed = false"
          >{{ unreadMessages }}</span
        >
      </transition>
      <div class="actions">
        <Reaction v-if="collapsed" />
        <button
          class="chat-setting button is-rounded is-outlined"
          @click="collapsed = !collapsed"
          :data-tooltip="collapsed ? 'Maximise' : 'Minimise'"
          :key="collapsed"
        >
          <span class="icon">
            <Icon v-if="collapsed" src="maximise.svg" size="20" />
            <Icon v-else src="minimise.svg" size="24" class="mt-4" />
          </span>
        </button>
        <button
          class="chat-setting button is-rounded is-outlined"
          @click="openChatSetting"
          data-tooltip="Settings"
        >
          <span class="icon">
            <Icon src="setting.svg" size="32" />
          </span>
        </button>
        <ClearChat option="public-chat" />
      </div>
      <div class="card-content" ref="theContent">
        <Messages :messages="messages" :style="{ fontSize }" />
      </div>
      <footer class="card-footer">
        <div class="card-footer-item">
          <div v-if="!collapsed" class="is-fullwidth my-1 reaction-bar">
            <Reaction :custom-emoji="true" />
            <div class="font-size-controls">
              <button
                class="button is-small is-rounded mx-1"
                data-tooltip="Increase font size"
                @click="increateFontSize()"
              >
                ➕
              </button>
              <button
                data-tooltip="Decrease font size"
                class="button is-small is-rounded mx-1"
                @click="decreaseFontSize()"
              >
                ➖
              </button>
            </div>
          </div>
          <div class="control has-icons-right is-fullwidth">
            <ChatInput
              v-model="message"
              placeholder="Type message"
              :loading="loadingUser"
              @submit="sendChat"
            />
          </div>
        </div>
      </footer>
    </div>
  </transition>
</template>

<script>
import { computed, onMounted, ref, watch, watchEffect } from "vue";
import anime from "animejs";
import { useStore } from "vuex";
import ChatInput from "components/form/ChatInput.vue";
import Icon from "components/Icon.vue";
import Reaction from "./Reaction.vue";
import Messages from "./Messages.vue";
import ClearChat from "./ClearChat.vue";

export default {
  components: { ChatInput, Reaction, Icon, Messages, ClearChat },
  setup: () => {
    const theContent = ref();
    const store = useStore();
    const chatVisibility = computed(
      () => store.state.stage.settings.chatVisibility,
    );
    const chatDarkMode = computed(
      () => store.state.stage.settings.chatDarkMode,
    );

    store.dispatch("stage/loadPermission");

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
        store.dispatch("stage/sendChat", { message: message.value });
        message.value = "";
        scrollToEnd();
      }
    };
    onMounted(scrollToEnd);
    watch(messages.value, scrollToEnd);
    watch(collapsed, (val) => {
      if (!val) {
        setTimeout(() => {
          scrollToEnd();
        });
      }
    });

    const openChatSetting = () =>
      store.dispatch("stage/openSettingPopup", {
        type: "ChatParameters",
      });

    const opacity = computed(() => store.state.stage.chat.opacity);
    const fontSize = computed(() => store.state.stage.chat.fontSize);

    const enter = (el, complete) => {
      anime({
        targets: el,
        scale: [0, 1],
        translateY: [-200, 0],
        complete,
      });
    };
    const leave = (el, complete) => {
      anime({
        targets: el,
        scale: 0,
        translateY: -200,
        complete,
      });
    };

    const increateFontSize = () => {
      let incValue = fontSize.value?.replace("px", "");
      incValue++;
      const parameters = {
        opacity: store.state.stage.chat.opacity,
        fontSize: `${incValue}px`,
      };
      store.commit("stage/SET_CHAT_PARAMETERS", parameters);
      setTimeout(
        () => (theContent.value.scrollTop = theContent.value.scrollHeight),
      );
    };

    const decreaseFontSize = () => {
      let decValue = fontSize.value?.replace("px", "");
      decValue > 1 && decValue--;
      const parameters = {
        opacity: store.state.stage.chat.opacity,
        fontSize: `${decValue}px`,
      };
      store.commit("stage/SET_CHAT_PARAMETERS", parameters);
    };
    const chatPosition = computed(() => store.state.stage.chatPosition);
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const stageSize = computed(() => store.getters["stage/stageSize"]);

    watchEffect(() => {
      if (!collapsed.value) {
        messages.value.forEach((message) => {
          if (!message.read) {
            message.read = true;
          }
        });
      }
    });
    const unreadMessages = computed(
      () => messages.value.filter((message) => !message.read).length,
    );
    const bounceUnread = (el) => {
      {
        anime({
          targets: el,
          scale: [1.2, 1],
          duration: 1000,
        });
      }
    };

    return {
      messages,
      message,
      sendChat,
      theContent,
      loadingUser,
      openChatSetting,
      collapsed,
      opacity,
      fontSize,
      chatVisibility,
      chatDarkMode,
      enter,
      leave,
      increateFontSize,
      decreaseFontSize,
      chatPosition,
      canPlay,
      stageSize,
      unreadMessages,
      bounceUnread,
    };
  },
};
</script>

<style lang="scss" scoped>
#chatbox {
  display: flex;
  flex-direction: column;
  position: fixed;
  min-width: 300px;
  bottom: 16px;
  right: 16px;
  overflow: visible;
  z-index: 3;
  @media only screen and (orientation: landscape) {
    height: calc(100% - 135px) !important;
  }
  @media only screen and (orientation: portrait) {
    width: calc(100vw - 32px) !important;
    .actions,
    .card-content,
    .card-footer {
      zoom: 3;
    }
    .actions {
      button:first-child {
        display: none;
      }
    }
  }

  .card-content {
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-top: 36px;
  }
  .card-footer-item {
    flex-wrap: wrap;
    padding-top: 0;
  }

  &.dark {
    background-color: #303030;
    color: #dddddd;

    .card-footer {
      border-top: 0.5px solid black;
    }

    :deep(.tag),
    :deep(.button),
    :deep(.textarea) {
      background-color: #303030 !important;
      border-color: #303030;
      color: #dddddd;
    }
    :deep(.textarea::placeholder) {
      color: #8c939a;
    }
    :deep(img) {
      filter: invert(100%) hue-rotate(180deg);
    }
    :deep(.guest .tag) {
      color: #8c939a;
    }

    .unread {
      background-color: #cc0f35 !important;
    }
  }

  &.collapsed {
    height: 108px !important;
    .card-content {
      padding: 0;
      height: 0;
      > div {
        display: none;
      }
    }
    .card-footer-item {
      padding-top: 6px;
    }
    .actions {
      top: 5px;
    }
  }

  .actions {
    position: absolute;
    right: 24px;
    top: 10px;
    z-index: 1;
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

  .unread {
    position: absolute;
    left: 12px;
    top: 6px;
  }
}
.reaction-bar {
  height: 30px;
  position: relative;
  .font-size-controls {
    position: absolute;
    top: 0;
    right: 0;
    .button.is-rounded {
      width: 16px;
    }
  }
}
</style>
