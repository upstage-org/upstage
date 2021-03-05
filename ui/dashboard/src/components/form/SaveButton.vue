<template>
  <button
    class="button is-primary"
    :class="{ 'is-loading': loading }"
    v-bind="$attrs"
  >
    <span class="icon is-small">
      <i class="fas fa-check"></i>
    </span>
    <span><slot>Save</slot></span>
  </button>
</template>

<script>
export default {
  props: ["loading"],
};
</script>

<style scoped>
.button {
  margin-left: auto;
  display: block;
}
</style>