<template>
  <Object :object="avatar" />
</template>

<script>
import Object from "./Object.vue";

export default {
  props: ["avatar"],
  components: { Object },
};
</script>

<style>
</style>