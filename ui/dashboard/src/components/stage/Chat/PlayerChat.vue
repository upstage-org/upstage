<template>
  <transition :css="false" @enter="enter" @leave="leave">
    <div
      id="player-chatbox"
      ref="theChatbox"
      v-show="playerChatVisibility"
      class="card is-light"
      :class="{ collapsed, 'is-movingable': isMovingable }"
      :style="{
        opacity,
        fontSize,
      }"
    >
      <div class="actions">
        <button
          class="chat-setting button is-rounded is-outlined"
          @click="minimiseToToolbox"
        >
          <span class="icon">
            <Icon v-if="collapsed" src="maximise.svg" size="20" />
            <Icon v-else src="minimise.svg" size="24" class="mt-4" />
          </span>
        </button>
        <button
          class="chat-setting button is-rounded is-outlined"
          :class="{ 'has-background-primary-light': isMovingable }"
          @click="toggleMoveable"
        >
          <span class="icon">
            <Icon src="prop.svg" size="20" />
          </span>
        </button>
        <ClearChat option="player-chat"/>
      </div>
      <div class="card-content" ref="theContent">
        <Messages :messages="messages" :style="{ fontSize }" />
      </div>
      <footer class="card-footer">
        <div class="card-footer-item">
          <div class="control has-icons-right is-fullwidth">
            <ChatInput
              v-model="chat.privateMessage"
              placeholder="Type message"
              :loading="loadingUser"
              :disabled="isMovingable"
              @submit="sendChat"
            />
          </div>
        </div>
      </footer>
    </div>
  </transition>
</template>

<script>
import { computed, onMounted, ref, watch } from "vue";
import anime from "animejs";
import { useStore } from "vuex";
import ChatInput from "@/components/form/ChatInput";
import Icon from "@/components/Icon";
import Messages from "./Messages";
import Moveable from "moveable";
import ClearChat from "./ClearChat";

export default {
  components: { ChatInput, Icon, Messages, ClearChat},
  setup: () => {
    const theChatbox = ref();
    const theContent = ref();
    const store = useStore();

    const messages = computed(() => store.state.stage.chat.privateMessages);
    const loadingUser = computed(() => store.state.user.loadingUser);
    const chat = store.state.stage.chat;
    const message = computed(() => store.state.stage.chat.privateMessage);
    const scrollToEnd = () => {
      anime({
        targets: theContent.value,
        scrollTop: theContent.value?.scrollHeight,
        easing: "easeInOutQuad",
      });
    };
    const sendChat = () => {
      if (message.value.trim() && !loadingUser.value) {
        store.dispatch("stage/sendChat", {
          message: message.value,
          isPrivate: true,
        });
        chat.privateMessage = "";
        scrollToEnd();
      }
    };
    watch(messages.value, scrollToEnd);
    onMounted(scrollToEnd);

    const opacity = computed(() => store.state.stage.chat.opacity);
    const fontSize = computed(() => store.state.stage.chat.fontSize);

    const enter = (el, complete) => {
      anime({
        targets: el,
        scaleY: [0, 1],
        translateX: [-200, 0],
        complete: () => {
          scrollToEnd();
          complete();
        },
      });
    };
    const leave = (el, complete) => {
      anime({
        targets: el,
        scaleY: 0,
        translateX: -200,
        easing: "easeInOutExpo",
        complete,
      });
    };

    const moveable = new Moveable(document.body, {
      draggable: true,
      resizable: true,
      origin: false,
    });

    onMounted(() => {
      moveable.on("drag", ({ target, left, top, height }) => {
        target.style.left = `${left}px`;
        if (
          top + height + 8 <
          (window.innerHeight || document.documentElement.clientHeight)
        ) {
          target.style.top = `${top}px`;
        }
      });
      moveable.on(
        "resize",
        ({ target, width, height, drag: { left, top } }) => {
          console.log(width, height);
          if (width > 100) {
            target.style.width = `${width}px`;
          }
          if (height > 120) {
            target.style.height = `${height}px`;
          }
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
        }
      );
    });

    const isMovingable = ref(false);
    const toggleMoveable = () => {
      moveable.setState({
        target: isMovingable.value ? null : theChatbox.value,
      });
      isMovingable.value = !isMovingable.value;
    };

    const playerChatVisibility = computed(
      () => store.state.stage.showPlayerChat
    );
    const minimiseToToolbox = () => {
      store.dispatch("stage/showPlayerChat", false);
      moveable.setState({ target: null });
      isMovingable.value = false;
    };

    return {
      messages,
      message,
      sendChat,
      theChatbox,
      theContent,
      loadingUser,
      opacity,
      fontSize,
      playerChatVisibility,
      enter,
      leave,
      toggleMoveable,
      isMovingable,
      minimiseToToolbox,
      chat,
    };
  },
};
</script>

<style lang="scss" scoped>
#player-chatbox {
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 56px;
  bottom: 16px;
  height: 200px;
  max-width: unset;
  overflow: visible;
  z-index: 3;

  .card-content {
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-top: 36px;
  }
  .card-footer-item {
    flex-wrap: wrap;
    padding-top: 6px;
    padding-bottom: 6px;
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
}
</style>