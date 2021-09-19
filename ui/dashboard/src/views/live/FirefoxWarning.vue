<template>
  <Modal v-if="visible">
    <template #trigger>
      <span
        class="tag is-small is-warning clickable"
        style="vertical-align: top"
      >
        <span class="icon" ref="icon">
          <Icon src="firefox-logo.svg" />
        </span>
      </span>
    </template>
    <template #header>
      <Icon size="24" src="firefox-logo.svg" /> Caution Firefox Users!
    </template>
    <template #content>
      <p>
        If you got stuck on CONNECTING, please turn off SPDY before you can use
        UpStage on Firefox:
      </p>
      <div class="columns">
        <div class="column is-3 mt-6">
          <b>Step 1: </b>Open a new tab and go to <code>about:config</code>
        </div>
        <div class="column">
          <img src="@/assets/firefox-instruction/1.png" alt="Step 1" />
        </div>
      </div>
      <div class="columns">
        <div class="column is-3 mt-6">
          <b>Step 2: </b>Search for <code>network.http.spdy.websockets </code>
        </div>
        <div class="column">
          <img src="@/assets/firefox-instruction/2.png" alt="Step 2" />
        </div>
      </div>
      <div class="columns">
        <div class="column is-3 mt-6">
          <b>Step 3: </b>Change the value to <code>false</code>
        </div>
        <div class="column">
          <img src="@/assets/firefox-instruction/3.png" alt="Step 3" />
        </div>
      </div>
    </template>
  </Modal>
</template>

<script>
import { computed, onUnmounted, ref } from "@vue/runtime-core";
import { useStore } from "vuex";
import Icon from "@/components/Icon.vue";
import Modal from "@/components/Modal.vue";
import anime from "animejs";

export default {
  components: { Icon, Modal },
  setup: () => {
    const store = useStore();
    const isFirefox = navigator.userAgent.indexOf("Firefox") != -1;
    const status = computed(() => store.state.stage.status);
    const visible = computed(() => isFirefox && status.value !== "LIVE");

    const reload = () => window.location.reload();

    const icon = ref();
    const interval = setInterval(() => {
      if (icon.value) {
        anime({
          targets: icon.value,
          scale: [1, 1.5, 1],
          rotate: [45, -45, 45, -45, 0],
          easing: "easeInOutQuad",
        });
      }
    }, 3000);

    onUnmounted(() => {
      clearInterval(interval);
    });
    return { isFirefox, status, reload, visible, icon };
  },
};
</script>

<style>
</style>