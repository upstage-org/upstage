<template>
  <transition name="fade">
    <div v-if="type" class="modal" :class="{ 'is-active': isActive }">
      <div class="modal-background" @click="close"></div>
      <div ref="modal" class="modal-content">
        <div class="card">
          <a href="#" class="card-header-icon" @click="close">
            <span class="icon">
              <i class="fas fa-times" aria-hidden="true"></i>
            </span>
          </a>
          <component :is="type" @close="close" />
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import Chat from "./settings/Chat";
import CreateStream from "./settings/CreateStream";
import CreateText from "./settings/CreateText";

export default {
  components: { Chat, CreateStream, CreateText },
  setup: () => {
    const store = useStore();
    const isActive = computed(() => store.state.stage.settingPopup.isActive);
    const type = computed(() => store.state.stage.settingPopup.type);
    const title = computed(() => store.state.stage.settingPopup.title);
    const modal = ref();

    const close = () => {
      store.dispatch("stage/closeSettingPopup");
    };
    return { isActive, close, modal, type, title };
  },
};
</script>
<style scoped lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.card-header-icon {
  position: absolute;
  right: 0;
}
</style>