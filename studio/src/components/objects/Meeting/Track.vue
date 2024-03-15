<script>
import { onMounted, onUnmounted, ref } from "vue";

export default {
  props: {
    track: Object,
  },
  setup(props) {
    const el = ref();
    onMounted(() => {
      props.track.attach(el.value);
    });
    onUnmounted(() => {
      props.track.detach();
    });
    if (props.track.getType() === "video") {
      return () => <video autoplay ref={el}></video>;
    } else {
      return () => <audio autoplay ref={el}></audio>;
    }
  },
};
</script>

<style scoped>
video {
  width: 200px;
  border-radius: 12px;
}
</style>
