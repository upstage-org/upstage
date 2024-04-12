<template>
  <p>
    Or follow this instruction if you're using OBS Studio. You can download OBS
    Studio
    <a href="https://obsproject.com/download" target="_blank">{{
      $t("here")
    }}</a
    >.
  </p>
  <div>
    <div class="mt-4">
      <b>Step 1:&nbsp;</b>Open OBS Studio and click
      <code class="text-red-600 bg-gray-200 p-1 text-sm">{{
        $t("settings")
      }}</code>
    </div>
    <div>
      <img
        class="w-full"
        :src="`${configs.UPSTAGE_URL}/instructions/obs/1.png`"
        alt="Step 1"
      />
    </div>
  </div>
  <div>
    <div class="mt-4">
      <b>Step 2:&nbsp;</b>In Stream tab, put the below configurations:
      <br />
      <b>Service:</b> Custom...
      <br />
      <b>Server:</b>
      <d-copy :value="publishUrl" />
      <br />
      <b>Stream Key:</b>
      <d-copy :value="streamKey" />
    </div>
    <div>
      <img
        class="w-full"
        :src="`${configs.UPSTAGE_URL}/instructions/obs/2.png`"
        alt="Step 2"
      />
    </div>
  </div>
  <div>
    <div class="mt-4">
      <b>Step 3:&nbsp;</b>Start Streaming! You should see the button changes to
      <code class="text-red-600 bg-gray-200 p-1 text-sm">{{
        $t("stop_streaming")
      }}</code>
      and LIVE counter started to work. If you have any issue, please contact
      UpStage Admin for help.
    </div>
    <div>
      <img
        class="w-full"
        :src="`${configs.UPSTAGE_URL}/instructions/obs/3.png`"
        alt="Step 3"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import configs from "config";
import { computed } from "vue";

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
  sign: {
    type: String,
    required: true,
  },
});

const publishUrl = configs.STREAMING.publish;
const streamKey = computed(() => {
  let key = props.url;
  if (key.includes("?")) {
    key = key.substring(0, key.indexOf("?"));
  }
  return `${key}?sign=${props.sign}`;
});
</script>

<style></style>
