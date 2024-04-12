<template>
  <Field
    v-bind="$attrs"
    :type="showPassword ? 'text' : 'password'"
    right="fas fa-eye"
  >
    <template #right>
      <Eye
        :slash="showPassword"
        @click="() => (showPassword = !showPassword)"
      />
      <a className="icon is-small is-right clickable" @click="() => (showPassword = !showPassword)">
        <i :class="`fas fa-${showPassword ? 'eye-slash' : 'eye'}`"></i>
      </a>
    </template>
  </Field>
</template>

<script lang="jsx">
import { ref } from "vue";
import Field from "./Field.vue";
export default {
  components: {
    Field
  },
  setup: () => {
    const showPassword = ref(false);
    return { showPassword };
  },
};
</script>

<style></style>
