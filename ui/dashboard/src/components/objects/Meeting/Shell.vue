<script>
import { provide } from 'vue';
import { useJitsi } from './composable'

export default {
  setup(_, { slots }) {
    const [jitsi, joined] = useJitsi();
    provide('jitsi', jitsi);
    provide('joined', joined);

    return () => <div>{() => slots.default()}</div>
  }
}
</script>