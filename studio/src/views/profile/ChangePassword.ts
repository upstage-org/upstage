import { defineComponent, h } from "vue";

export const ChangePassword = defineComponent({
  props: {
    teddy: {
      type: String,
      required: true,
      validator(value) {
        return String(value).trim().length > 0;
      },
    },
  },
  setup(props, ctx) {
    return () => h("div", ["Hi"]);
  },
});
