<script>
import Skeleton from "components/stage/Toolbox/Skeleton.vue";
import { computed, inject, onMounted, reactive, ref, watch } from "vue";
import { useStore } from "vuex";
import { useLowLevelAPI } from "./composable";

export default {
  setup() {
    const store = useStore();
    const stageSize = computed(() => store.getters["stage/stageSize"]);

    let tracks = [];
    const el = ref();
    const blocked = ref(false);
    const data = reactive({
      type: "stream",
      jitsi: true,
      name: store.state.user.user?.email,
      description: store.state.user.user?.email,
      w: stageSize.value.width / 2,
      h: stageSize.value.height / 2,
    });

    const jitsi = inject("jitsi");
    const joined = inject("joined");
    const JitsiMeetJS = useLowLevelAPI();

    onMounted(() => {
      JitsiMeetJS.createLocalTracks({ devices: ["audio", "video"] })
        .then((track) => {
          for (const t of track) {
            tracks.push(t);
            if (t.type === "video") {
              t.attach(el.value);
              // el.value.addEventListener("loadedmetadata", () => {
              //   const width = el.value.videoWidth;
              //   const height = el.value.videoHeight;
              //   //data.w = (100 * width) / height;
              //   //data.h = 100;
              // });
            }
          }
        })
        .catch((err) => {
          console.error(
            "Failed to create local tracks. Please check your camera and microphone permissions.",
            err,
          );
          blocked.value = true;
        });
    });

    watch(joined, () => (data.participantId = jitsi.room?.myUserId()), {
      immediate: true,
    });

    const join = () => {
      if (joined.value) {
        for (const t of tracks) {
          jitsi.room.addTrack(t);
        }
      }
    };

    const nickname = computed(() => store.getters["user/nickname"]);
    return {
      blocked,
      data,
      join,
      joined,
      el,
      nickname
    }
  },
};
</script>
<template>
  <Skeleton :data="data" class="p-2" :onDragstart="join" style="flex-direction: column;">
    <Icon v-if="blocked" src="backdrop.svg" height="48" width="36" />
    <video v-else :style="{ cursor: joined ? 'pointer' : 'not-allowed', height: '44px', marginBottom: '4px' }"
      :onClick="join" autoplay ref="el"></video>
    <span class="tag">{{ $t("new_stream") }}</span>
  </Skeleton>
</template>
<style scoped>
video {
  width: 100px;
  border-radius: 8px;
}
</style>
