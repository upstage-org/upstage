<template>
  <button
    class="button is-primary"
    :class="{ 'is-loading': loading }"
    v-bind="$attrs"
  >
    <slot>
      <span class="icon is-small">
        <i class="fas fa-check"></i>
      </span>
      <span>{{ $t("save") }}</span>
    </slot>
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
