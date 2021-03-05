<template>
  <button
    class="button is-primary"
    :class="{ 'is-loading': loading }"
    @click="$emit('click')"
  >
    <span class="icon is-small">
      <i class="fas fa-check"></i>
    </span>
    <span><slot>Save</slot></span>
  </button>
</template>

<script>
export default {
  emits: ["click", "loading"],
};
</script>

<style scoped>
.button {
  margin-left: auto;
  display: block;
}
</style>