<template>
  <template v-if="reactionVisibility">
    <button
      class="button is-small is-rounded reaction mx-1"
      v-for="react in reactions"
      :key="react"
      @click="sendReaction(react)"
    >
      {{ react }}
    </button>
    <span v-if="customEmoji" style="position: absolute; margin-left: 28px">
      <ChatInput
        :picker-only="true"
        :style="{ height: '30px' }"
        className="is-white"
        @update:model-value="sendCustomReaction"
      >
        <template #icon>
          <span class="icon" data-tooltip="Custom Reactions">
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
  <div class="my-1" style="float: left" v-else>
    Your nickname is:
    <a @click="openChatSetting">{{ nickname }}</a>
  </div>
</template>

<script>
import { computed, watch } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import ChatInput from "components/form/ChatInput.vue";
import Icon from "components/Icon.vue";

export default {
  components: { ChatInput, Icon },
  props: ["customEmoji"],
  setup: () => {
    const store = useStore();
    const reactionVisibility = computed(
      () => store.state.stage.settings.reactionVisibility,
    );
    watch(reactionVisibility, console.log);
    const nickname = computed(() => {
      const nickname = store.getters["user/nickname"];
      if (nickname.length > 15) {
        return nickname.slice(0, 10) + "...";
      }
      return nickname;
    });

    const reactions = ["❤️", "🤣", "🙌", "👏"];
    const sendReaction = (react) => {
      store.dispatch("stage/sendReaction", react);
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

    const openChatSetting = () =>
      store.dispatch("stage/openSettingPopup", {
        type: "ChatParameters",
      });

    return {
      reactions,
      sendReaction,
      flyingReactions,
      flyin,
      flyout,
      sendCustomReaction,
      reactionVisibility,
      nickname,
      openChatSetting,
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
