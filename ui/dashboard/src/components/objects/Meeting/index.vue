<template>
  <div>
    <Object :object="meeting">
      <template #render>
        <Loading v-if="loading" height="100%" />
        <div class="room" ref="room"></div>
      </template>
    </Object>
  </div>
</template>

<script>
import Object from "../Object.vue";
import Loading from "@/components/Loading.vue";
import { computed, onMounted, ref } from "vue";

export default {
  components: { Object, Loading },
  props: ["object"],
  setup: (props) => {
    const room = ref();
    const meeting = computed(() => props.object);

    onMounted(() => {
      const domain = 'meet.jit.si';
      const options = {
        roomName: 'JitsiMeetAPIExample',
        width: props.object.w,
        height: props.object.h,
        parentNode: room.value,
      };
      const api = new window.JitsiMeetExternalAPI(domain, options);
      console.log(api);
    })

    return { meeting, room };
  },
};
</script>

<style lang="scss" scoped>
.room,
.room iframe {
  width: 100%;
  height: 100%;
}
</style>