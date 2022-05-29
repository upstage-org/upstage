<script>
import Skeleton from '@/components/stage/Toolbox/Skeleton.vue';
import { computed, inject, onMounted, reactive, ref, watch } from 'vue';
import { useStore } from 'vuex';
import { useLowLevelAPI } from './composable'

export default {
  setup() {
    let tracks = [];
    const el = ref();
    const blocked = ref(false);
    const data = reactive({ type: 'jitsi', participantId: null, w: 100, h: 100 });

    const jitsi = inject('jitsi');
    const joined = inject('joined');
    const JitsiMeetJS = useLowLevelAPI();

    onMounted(() => {
      JitsiMeetJS.createLocalTracks({ devices: ['audio', 'video'] }).then(track => {
        for (const t of track) {
          tracks.push(t);
          if (t.type === 'video') {
            t.attach(el.value);
            el.value.addEventListener("loadedmetadata", () => {
              const width = el.value.videoWidth;
              const height = el.value.videoHeight;
              data.w = 100 * width / height;
              data.h = 100;
            });
          }
        }
      }).catch(err => {
        console.error('Failed to create local tracks. Please check your camera and microphone permissions.', err);
        blocked.value = true;
      });
    })

    watch(joined, () => data.participantId = jitsi.room.myUserId(), { immediate: true });

    const join = () => {
      if (joined.value) {
        for (const t of tracks) {
          jitsi.room.addTrack(t);
        }
      }
    }

    const store = useStore();
    const nickname = computed(() => store.getters['user/nickname']);

    return () => blocked.value ? <></> : <Skeleton data={data} class="p-2" onDragstart={join}>
      <video style={{ cursor: joined.value ? 'pointer' : 'not-allowed' }} onClick={join} autoplay ref={el}></video>
      <span class="tag">{nickname.value}</span>
    </Skeleton>
  }
}
</script>

<style scoped>
video {
  width: 100px;
  border-radius: 8px;
}
</style>