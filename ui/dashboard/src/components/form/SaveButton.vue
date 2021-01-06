<template>
  <button class="button is-primary" @click="$emit('click')">
    <span class="icon is-small">
      <i class="fas fa-check"></i>
    </span>
    <span><slot>Save</slot></span>
  </button>
</template>

<script>
export default {
  emits: ["click"],
};
</script>

<style scoped>
.button {
  margin-left: auto;
  display: block;
}
</style>