<template>
  <div v-if="stream.url" class="card-content">
    <div class="columns">
      <div class="column">
        <button v-if="!stream.metadata" class="button is-light is-loading is-fullwidth"
          style="height: 25vh">Loading</button>
        <video ref="video" v-show="stream.metadata" preload="auto" controls :src="stream.url"
          @loadeddata="handleData"></video>
      </div>
      <div class="column">
        <template v-if="stream.metadata">
          <p class="mb-4">
          <ul>
            <li>Duration: {{Math.round(stream.metadata.duration)}}s</li>
            <li>Width: {{stream.metadata.videoWidth}}</li>
            <li>Height: {{stream.metadata.videoHeight}}</li>
          </ul>
          </p>
          <p>
            <img :src="stream.src"/>
          </p>
        </template>
        <p class="title mb-2">Stream URL</p>
        <p class="mb-4">
          <span class="title"></span>
          <input-button-postfix :placeholder="stream.url" icon="fas fa-check" @ok="value => stream.url = value" />
        </p>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <save-button :disabled="stream.loading" @click="save" />
      </div>
    </div>
  </div>
  <div v-else class="card-content">
    <p class="title">Enter Stream URL</p>
    <p>
      <input-button-postfix icon="fas fa-check" @ok="value => stream.url = value"
        placeholder="https://www.w3schools.com/html/mov_bbb.mp4" />
    </p>
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import InputButtonPostfix from "@/components/form/InputButtonPostfix";
import SaveButton from "@/components/form/SaveButton.vue";
import { useStore } from "vuex";

export default {
  components: { InputButtonPostfix, SaveButton },
  setup: (props, { emit }) => {
    const store = useStore();
    const video = ref();
    const stream = reactive({
      loading: true,
    });

    const handleData = (e) => {
      stream.metadata = e.target;
      stream.loading = false;
    };

    const save = () => {
      stream.type = "stream";
      store.dispatch("stage/addStream", stream).then(() => emit("close"));
    };

    return { video, stream, handleData, save };
  },
};
</script>

<style>
.card-footer-item {
  cursor: pointer;
}
</style>