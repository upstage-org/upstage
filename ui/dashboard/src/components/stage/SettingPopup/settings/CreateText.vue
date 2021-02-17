<template>
  <div class="card-content">
    <p class="title">Text Tool</p>
    <p contenteditable="true" :style="options">Write or paste your text here</p>
    <save-button @click="save" class="mt-4" />
  </div>
</template>

<script>
import SaveButton from "@/components/form/SaveButton";
import { useStore } from "vuex";
import { computed } from "vue";
export default {
  components: { SaveButton },
  setup: () => {
    const store = useStore();
    const options = computed(() => store.state.stage.preferences.text);

    return { options };
  },
};
</script>

<style>
</style>