<script lang="ts">
import Navbar from "components/Navbar.vue";
import { h } from "vue";
import { Affix, Space } from "ant-design-vue";

export default {
  setup(_, { slots }) {
    return () =>
      h(Affix, { offsetTop: 0 }, [
        h(
          Space,
          {
            class: "shadow rounded-xl px-4 py-2 bg-white flex justify-between",
          },
          [slots.default?.(), h(Navbar)],
        ),
      ]);
  },
};
</script>
