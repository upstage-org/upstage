<template>
  <div v-if="editing" class="control has-icons-right is-fullwidth">
    <input
      class="input is-medium is-rounded"
      placeholder="New Stage Name"
      v-model="stageName"
      @keydown.enter="duplicateStage"
      @keydown.esc="() => (editing = false)"
    />
    <span
      class="icon is-right clickable button is-primary is-rounded"
      @click="duplicateStage"
    >
      <i class="fas fa-check"></i>
    </span>
  </div>
  <template v-else>
    <router-link
      to="/dashboard/stage-management"
      class="button mx-2 is-block is-fullwidth is-primary"
    >
      <span class="icon">
        <i class="fa fa-cog"></i>
      </span>
      <span>Manage</span>
    </router-link>
    <button
      class="button mx-2 is-block is-fullwidth is-dark"
      @click="() => (editing = true)"
    >
      <span class="icon">
        <i class="fa fa-copy"></i>
      </span>
      <span>Duplicate</span>
    </button>
    <button class="button mx-2 is-block is-fullwidth is-danger">
      <span class="icon">
        <i class="fa fa-times"></i>
      </span>
      <span>Delete</span>
    </button>
  </template>
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
</style>