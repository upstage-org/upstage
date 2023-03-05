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
    </template>
  </Field>
</template>

<script>
import { ref } from "vue";
import Field from "./Field";
export default {
  components: {
    Field,
    Eye: (props) => (
      <a className="icon is-small is-right clickable" onClick={props.onClick}>
        <i className={`fas fa-${props.slash ? "eye-slash" : "eye"}`}></i>
      </a>
    ),
  },
  setup: () => {
    const showPassword = ref(false);
    return { showPassword };
  },
};
</script>

<style></style>
