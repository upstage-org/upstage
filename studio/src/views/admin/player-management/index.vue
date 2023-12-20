<script lang="ts">
import PlayerFilter from "./PlayerFilter.vue";
import PlayerTable from "./PlayerTable.vue";
import { h } from "vue";

export default {
  setup(props, ctx) {
    return () => [h(PlayerFilter), h(PlayerTable)];
  },
};
</script>
