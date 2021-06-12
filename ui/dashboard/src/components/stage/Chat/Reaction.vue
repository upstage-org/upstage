<template>
  <button
    class="button is-small is-rounded reaction mx-1"
    v-for="react in reactions"
    :key="react"
    @click="sendReaction(react)"
  >
    {{ react }}
  </button>
  <button
    class="button is-small is-rounded reaction mx-1"
    :key="encrease - fontSize"
    @click="increateFontSize()"
  >
    {{ "➕" }}
  </button>
  <button
    class="button is-small is-rounded reaction mx-1"
    :key="decrease - fontSize"
    @click="decreaseFontSize()"
  >
    {{ "➖" }}
  </button>
  <span v-if="customEmoji">
    <ChatInput
      :picker-only="true"
      :style="{ height: '30px' }"
      className="is-white"
      @update:model-value="sendCustomReaction"
    >
      <template #icon>
        <span class="icon">
          <Icon src="new.svg" />
        </span>
      </template>
    </ChatInput>
  </span>
  <teleport to="body">
    <div class="flying-reactions">
      <transition-group :css="false" @enter="flyin" @leave="flyout">
        <div
          v-for="react in flyingReactions"
          :key="react"
          :style="{
            position: 'fixed',
            left: react.x + 'px',
            top: react.y + 'px',
            fontSize: '42px',
          }"
        >
          {{ react.reaction }}
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script>
import { computed, reactive } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import ChatInput from "@/components/form/ChatInput";
import Icon from "@/components/Icon";

export default {
  components: { ChatInput, Icon },
  props: ["customEmoji"],
  setup: () => {
    const store = useStore();

    const reactions = ["❤️", "🤣", "🙌", "👏"];
    const sendReaction = (react) => {
      store.dispatch("stage/sendReaction", react);
    };

    const fontSize = computed(() => store.state.stage.chat.fontSize);
    const increateFontSize = () => {
      let incValue = fontSize.value?.replace("px", "");
      incValue++;
      const parameters = reactive({
        opacity: store.state.stage.chat.opacity,
        fontSize: `${incValue}px`,
      });
      store.commit("stage/SET_CHAT_PARAMETERS", parameters);
    };

    const decreaseFontSize = () => {
      let decValue = fontSize.value?.replace("px", "");
      decValue > 1 && decValue--;
      const parameters = reactive({
        opacity: store.state.stage.chat.opacity,
        fontSize: `${decValue}px`,
      });
      store.commit("stage/SET_CHAT_PARAMETERS", parameters);
    };

    const flyingReactions = computed(() => store.state.stage.reactions);

    const flyin = (el) => {
      anime({
        targets: el,
        translateY: [100, 0],
        scale: [1, 1.5, 1],
      });
    };
    const flyout = (el, complete) => {
      anime({
        targets: el,
        scale: 0,
        rotate: 180,
        translateY: 100,
        duration: 2000,
        complete,
      });
    };

    const sendCustomReaction = (e) => {
      sendReaction(e);
    };

    return {
      reactions,
      sendReaction,
      flyingReactions,
      flyin,
      flyout,
      sendCustomReaction,
      increateFontSize,
      decreaseFontSize,
    };
  },
};
</script>

<style lang="scss" scoped>
.flying-reactions {
  position: fixed;
}
.button.is-rounded {
  width: 16px;
}
</style>