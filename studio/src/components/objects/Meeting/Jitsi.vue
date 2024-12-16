<template>
  <Object :object="object">
    <template #render>
      <Loading v-if="!videoTrack && !audioTrack" height="100%" />
      <template v-else>
        <video autoplay ref="videoEl" :style="{
          'border-radius': object.shape === 'circle' ? '100%' : '12px',
        }" @loadedmetadata="logDuration"></video>
        <audio autoplay ref="audioEl" :muted="localMuted"></audio>
        <button v-if="isPlayer" class="button is-small mute-icon clickable" @mousedown="toggleMuted">
          <i v-if="localMuted" class="fas fa-volume-mute has-text-danger"></i>
          <i v-else class="fas fa-volume-up has-text-primary"></i>
        </button>
      </template>
    </template>
    <template #menu="slotProps">
      <div class="field has-addons shape-group">
        <p class="control menu-group-item">Shape</p>
        <p class="control menu-group-item">
          <button class="button is-light" @click="clip(null)">
            <div class="icon">
              <i class="fas fa-square"></i>
            </div>
          </button>
        </p>
        <p class="control menu-group-item" @click="clip('circle')">
          <button class="button is-light">
            <div class="icon">
              <i class="fas fa-circle"></i>
            </div>
          </button>
        </p>
      </div>
      <AvatarContextMenu :object="object" v-bind="slotProps" />
    </template>
  </Object>
</template>

<script>
import Object from "../Object.vue";
import Loading from "components/Loading.vue";
import { computed, inject, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import AvatarContextMenu from "../Avatar/ContextMenu.vue";

export default {
  components: { Object, Loading, AvatarContextMenu },
  props: ["object"],
  setup: (props) => {
    const store = useStore();
    const videoEl = ref();
    const audioEl = ref();
    const tracks = computed(() =>
      store.getters["stage/jitsiTracks"].filter(
        (t) => t.getParticipantId() === props.object.participantId,
      ),
    );
    const videoTrack = computed(() =>
      tracks.value.find((t) => t.type === "video" && t.stream.active),
    );
    const audioTrack = computed(() =>
      tracks.value.find((t) => t.type === "audio" && t.stream.active),
    );
    const loadTrack = () => {
      if (tracks.value.length) {
        setTimeout(() => {
          try {
            if (videoTrack.value) {
              videoTrack.value.attach(videoEl.value);
            }
            if (audioTrack.value && !audioTrack.value.isLocal()) {
              audioTrack.value.attach(audioEl.value);
            }
          } catch (error) {
            console.log("Error on attaching track", error);
          }
        }, 500)
      }
    };
    watch(tracks, (newValue, oldValue) => {
      if (oldValue.length <= 0)
        loadTrack();
    });
    const joined = inject("joined");
    const jitsi = inject("jitsi");

    watch(
      joined,
      (val) => {
        if (val) {
          const participants = jitsi.room
            .getParticipants()
            .map((p) => p.getId())
            .concat(jitsi.room.myUserId());
          if (!participants.some((p) => p === props.object.participantId)) {
            store.dispatch("stage/deleteObject", props.object);
          }
        }
      },
      { immediate: true },
    );

    onMounted(loadTrack);

    const clip = (shape) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        shape,
      });
    };

    const localMuted = ref(false);
    const toggleMuted = () => {
      localMuted.value = !localMuted.value;
    };
    const isPlayer = computed(() => store.getters["stage/canPlay"]);

    const logDuration = (e) => {
      console.log('==============duration', videoEl)
    }
    return {
      videoTrack,
      audioTrack,
      videoEl,
      audioEl,
      clip,
      localMuted,
      toggleMuted,
      isPlayer,
      logDuration
    };
  },
};
</script>

<style lang="scss" scoped>
video {
  width: 100%;
}
</style>

<style lang="scss" scoped>
.mute-icon {
  position: absolute;
  width: 24px;
  height: 20px;
  bottom: 8px;
  right: 8px;

  &:hover {
    transform: scale(1.2);
  }
}

.shape-group {
  width: 100%;
  display: flex;
  align-items: center;
  text-align: center;

  .menu-group-item {
    flex: 1;

    button {
      width: 100%;
    }
  }
}
</style>
