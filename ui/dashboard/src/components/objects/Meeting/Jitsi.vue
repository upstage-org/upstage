<template>
  <Object :object="object">
    <template #render>
      <Loading v-if="!videoTrack && !audioTrack" height="100%" />
      <template v-else>
        <video autoplay ref="videoEl"></video>
        <audio autoplay ref="audioEl"></audio>
      </template>
    </template>
  </Object>
</template>

<script>
import Object from "../Object.vue";
import Loading from "@/components/Loading.vue";
import { computed, inject, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";

export default {
  components: { Object, Loading },
  props: ["object"],
  setup: (props) => {
    const store = useStore();
    const videoEl = ref();
    const audioEl = ref();
    const tracks = computed(() => store.getters['stage/jitsiTracks'].filter(t => t.getParticipantId() === props.object.participantId));
    const videoTrack = computed(() => tracks.value.find(t => t.type === 'video'));
    const audioTrack = computed(() => tracks.value.find(t => t.type === 'audio'));

    const loadTrack = () => {
      if (tracks.value.length) {
        try {
          if (videoTrack.value) {
            videoTrack.value.attach(videoEl.value);
          }
          if (audioTrack.value && !audioTrack.value.isLocal()) {
            audioTrack.value.attach(audioEl.value);
          }
        } catch (error) {
          console.log('Error on attaching track', error);
        }
      }
    }

    const joined = inject('joined');
    const jitsi = inject('jitsi');

    watch(joined, val => {
      if (val) {
        const participants = jitsi.room.getParticipants().map(p => p.getId()).concat(jitsi.room.myUserId());
        if (!participants.some(p => p === props.object.participantId)) {
          store.dispatch('stage/deleteObject', props.object);
        }
      }
    }, { immediate: true })

    onMounted(loadTrack);
    watch(tracks, loadTrack);

    return { videoTrack, audioTrack, videoEl, audioEl };
  },
};
</script>

<style lang="scss" scoped>
video {
  width: 100%;
  border-radius: 12px;
}
</style>