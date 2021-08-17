<template>
  <Modal>
    <template #trigger>
      <p
        title="Show instruction on OBS Studio"
        class="has-tooltip-bottom clickable"
      >
        <Icon size="50" src="obs-logo.png" />
      </p>
    </template>
    <template #header>
      <Icon size="24" src="obs-logo.png" />
      How to stream to UpStage using OBS Studio
    </template>
    <template #content>
      <p>
        OBS Studio is a free and open source software for video recording and
        live streaming. You can download OBS Studio
        <a href="https://obsproject.com/download" target="_blank">here</a>.
      </p>
      <div class="columns">
        <div class="column is-4 mt-6">
          <b>Step 1: </b>Open OBS Studio and click <code>Settings</code>
        </div>
        <div class="column">
          <img src="@/assets/obs-instruction/1.png" alt="Step 1" />
        </div>
      </div>
      <div class="columns">
        <div class="column is-4 mt-6">
          <b>Step 2: </b>In Stream tab, choose Custom... for Service,
          <code>{{ publishUrl }}</code> for Server and
          <code>{{ url }}?sign={{ sign }}</code> for Stream Key.
        </div>
        <div class="column">
          <img src="@/assets/obs-instruction/2.png" alt="Step 2" />
        </div>
      </div>
      <div class="columns">
        <div class="column is-4 mt-6">
          <b>Step 3: </b>Start Streaming! You should see the button changes to
          <code>Stop Streaming</code> and LIVE counter started to work. If you
          have any issue, please contact UpStage Admin for help.
        </div>
        <div class="column">
          <img src="@/assets/obs-instruction/3.png" alt="Step 3" />
        </div>
      </div>
    </template>
  </Modal>
</template>

<script>
import Icon from "@/components/Icon.vue";
import Modal from "@/components/Modal.vue";
import configs from "@/config";

export default {
  components: { Icon, Modal },
  props: ["url", "sign"],
  setup: () => {
    return { publishUrl: configs.STREAMING.publish };
  },
};
</script>

<style>
</style>