<template>
  <div v-if="editing" class="control has-icons-right is-fullwidth">
    <input
      class="input is-medium is-rounded"
      placeholder="New Stage Name"
      v-model="stageName"
      @keydown.enter="duplicateStage"
    />
    <span
      class="icon is-right duplicate-button button is-primary is-rounded"
      @click="duplicateStage"
    >
      <i class="fas fa-check"></i>
    </span>
  </div>
  <button
    v-else
    class="button mx-2 is-block is-fullwidth is-primary"
    @click="() => (editing = true)"
  >
    <span class="icon">
      <i class="fa fa-plus"></i>
    </span>
    <span>Duplicate</span>
  </button>
</template>

<script>
import { ref } from "vue";
export default {
  setup: () => {
    const editing = ref(false);
    const stageName = ref("");
    const duplicateStage = () => {
      console.log("Duplicated " + stageName.value);
      editing.value = false;
    };

    return { editing, duplicateStage, stageName };
  },
};
</script>

<style>
.duplicate-button {
  pointer-events: all !important;
}
</style>