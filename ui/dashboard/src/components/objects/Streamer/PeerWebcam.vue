<template>
  <video autoplay="true" ref="video"></video>
</template>

<script>
import config from "@/config";
import { ref } from "@vue/reactivity";
export default {
  props: ["object"],
  setup(props) {
    const video = ref();
    console.log(props.object.rtc);
    const pc2 = new RTCPeerConnection(config.RTC.iceConfiguration);
    pc2.addEventListener("icecandidate", () => {
      pc2.addIceCandidate(props.object.rtc.candidate);
    });
    pc2.ontrack = (event) => {
      if (video.value.srcObject !== event.streams[0]) {
        video.value.srcObject = event.streams[0];
        video.value.play();
      }
    };
    pc2
      .setRemoteDescription(props.object.rtc.desc)
      .then(() => pc2.createAnswer())
      .then((answerDesc) => pc2.setLocalDescription(answerDesc))
      .then();

    return { pc2, video };
  },
};
</script>

<style>
</style>