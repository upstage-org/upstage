<template>
  <div class="yard">
    <Track v-for="track in tracks" :key="track.getId()" :track="track" />
  </div>
</template>

<script setup>
import Track from "components/objects/Meeting/Track.vue";
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
const tracks = computed(() => store.getters["stage/jitsiTracks"]);
</script>

<style scoped>
.yard {
  display: flex;
  justify-content: space-around;
}
</style>
