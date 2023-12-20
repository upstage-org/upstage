<template>
  <Modal v-if="visible" v-model="open">
    <template #trigger>
      <span class="tag is-small is-warning clickable" style="vertical-align: top">
        <span class="icon" ref="icon">
          <Icon src="firefox-logo.svg" />
        </span>
      </span>
    </template>
    <template #header>
      <Icon size="24" src="firefox-logo.svg" />&nbsp;Caution Firefox Users!
    </template>
    <template #content>
      <p>A Firefox setting needs to be changed to allow you to access UpStage on Firefox.</p>
      <div class="columns">
        <div class="column is-3 mt-6">
          <b>Step 1:</b>&nbsp;Open a new tab and go to
          <Copy value="about:config" />
        </div>
        <div class="column">
          <img :src="`${publicPath}/instruction/firefox/1.png`" alt="Step 1" />
          <div class="columns">
            <div class="column is-4 mt-6">
              <code>Note:</code>&nbsp;If you see this screen, click to continue. Don't worry, the setting change needed for UpStage to work will not impact on performance or security of Firefox.
            </div>
            <div class="column">
              <img :src="`${publicPath}/instruction/firefox/1.2.png`" alt="Step 1.2" />
            </div>
          </div>
        </div>
      </div>
      <div class="columns">
        <div class="column is-4 mt-6">
          <b>Step 2:</b>&nbsp;Search for
          <Copy value="network.http.spdy.websockets" />
        </div>
        <div class="column">
          <img :src="`${publicPath}/instruction/firefox/2.png`" alt="Step 2" />
        </div>
      </div>
      <div class="columns">
        <div class="column is-4 mt-6">
          <b>Step 3:</b>&nbsp;Change the value to
          <code>false</code>
        </div>
        <div class="column">
          <img :src="`${publicPath}/instruction/firefox/3.png`" alt="Step 3" />
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
import Copy from "@/components/Copy.vue";
import anime from "animejs";
import { publicPath } from '@/../vue.config';

export default {
  components: { Icon, Modal, Copy },
  setup: () => {
    const store = useStore();
    const isFirefox = navigator.userAgent.indexOf("Firefox") != -1;
    const status = computed(() => store.state.stage.status);
    const visible = computed(() => isFirefox && (status.value === "CONNECTING" || status.value === "OFFLINE"));
    const open = ref(true);

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
    return { isFirefox, status, reload, visible, icon, open, publicPath };
  },
};
</script>

<style>
</style>