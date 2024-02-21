<template>
  <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
    <div class="column has-text-centered has-text-light">
      <i class="fas fa-comments fa-4x"></i>
      <p class="subtitle has-text-light">No messages yet!</p>
    </div>
  </div>
  <div v-else>
    <p v-for="item in messages" :key="item" :class="{ guest: !item.isPlayer }">
      <template v-if="item.clear">
        <Divider>{{ $t("clear_chat") }}</Divider>
      </template>
      <template v-else-if="item.clearPlayerChat">
        <Divider>{{ $t("clear_chat") }}</Divider>
      </template>
      <template v-else>
        <ContextMenu>
          <template #trigger>
            <div style="position: relative">
              <small style="font-size: 1em">
                <b v-if="item.isPlayer">{{ item.user }}:</b>
                <span v-else>{{ item.user }}:</span>
              </small>
              <span
                class="tag message"
                :style="{
                  'font-size': '1em',
                }"
                :class="
                  messageClass[item.highlighted ? 'highlighted' : item.behavior]
                "
                :title="time(item.at)"
              >
                <span
                  v-if="item.highlighted"
                  :data-tooltip="
                    canPlay
                      ? 'Click to remove highlight'
                      : 'This is a highlight message'
                  "
                  class="highlight-star has-tooltip-left"
                  @click="highlightChat(item)"
                >
                  <i class="far fa-star has-text-warning"></i>
                </span>
                <Linkify>{{ item.message }}</Linkify>
              </span>
            </div>
          </template>
          <template
            v-if="canPlay || session === item.session"
            #context="{ closeMenu }"
          >
            <div class="panel-block">
              <span>
                <Linkify>{{ item.message }}</Linkify>
                <div>
                  <small class="has-text-dark">
                    Sent by
                    <span v-if="session === item.session">{{ $t("you") }}</span>
                    <span v-else>{{ item.user }}</span>
                    {{ time(item.at) }}
                  </small>
                </div>
              </span>
            </div>
            <template v-if="item.id">
              <a
                class="panel-block has-text-danger"
                @click="removeChat(item, closeMenu)"
              >
                <span class="panel-icon">
                  <Icon src="remove.svg" />
                </span>
                <span>{{ $t("remove") }}</span>
              </a>
              <template v-if="canPlay">
                <a
                  v-if="item.highlighted"
                  class="panel-block"
                  @click="highlightChat(item, closeMenu)"
                >
                  <span class="panel-icon">
                    <Icon src="object-drawing.svg" />
                  </span>
                  <span>{{ $t("unhighlight") }}</span>
                </a>
                <a
                  v-else
                  class="panel-block has-text-primary"
                  @click="highlightChat(item, closeMenu)"
                >
                  <span class="panel-icon">
                    <Icon src="object-drawing.svg" />
                  </span>
                  <span>{{ $t("highlight") }}</span>
                </a>
              </template>
            </template>
            <div v-else class="panel-block has-text-dark">
              <span class="panel-icon">
                <Icon src="clear.svg" />
              </span>
              <small
                >Sorry but no actions can be performed against these legacy
                messages!</small
              >
            </div>
          </template>
        </ContextMenu>
      </template>
    </p>
  </div>
</template>

<script>
import moment from "moment";
import Linkify from "@/components/Linkify";
import Divider from "@/components/Divider";
import ContextMenu from "@/components/ContextMenu";
import Icon from "@/components/Icon.vue";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  props: ["messages", "style"],
  components: { Linkify, Divider, ContextMenu, Icon },
  setup: () => {
    const store = useStore();
    const messageClass = {
      think: "has-text-info has-background-info-light",
      shout: "has-text-danger",
      highlighted: "has-background-warning",
    };
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const session = computed(() => store.state.stage.session);

    const time = (value) => {
      return moment(value).fromNow();
    };

    const removeChat = (item, closeMenu) => {
      store.dispatch("stage/removeChat", item.id).then(closeMenu);
    };

    const highlightChat = (item, closeMenu) => {
      if (canPlay.value) {
        store.dispatch("stage/highlightChat", item.id).then(closeMenu);
      }
    };

    return { messageClass, time, removeChat, highlightChat, canPlay, session };
  },
};
</script>

<style lang="scss">
.tag.message {
  white-space: break-spaces;
  height: unset;
  .highlight-star {
    position: absolute;
    right: -16px;
  }
}
.guest {
  opacity: 0.5;
}
</style>
