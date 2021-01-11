<template>
  <transition name="fade">
    <div v-if="type" class="modal" :class="{ 'is-active': isActive }">
      <div class="modal-background" @click="close"></div>
      <div ref="modal" class="modal-content">
        <div class="card">
          <header class="card-header">
            <p class="card-header-title">{{ title }}</p>
            <a href="#" class="card-header-icon" @click="close">
              <span class="icon">
                <i class="fas fa-times" aria-hidden="true"></i>
              </span>
            </a>
          </header>
          <div class="card-content">
            <div class="content">
              <component :is="type" @close="close" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import Chat from "./settings/Chat";

export default {
  components: { Chat },
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
</style>