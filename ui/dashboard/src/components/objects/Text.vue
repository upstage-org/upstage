<template>
  <Object :object="text">
    <template #menu="slotProps">
      <MenuContent
        :object="text"
        :closeMenu="slotProps.closeMenu"
        v-model:active="active"
      />
    </template>
    <template #render>
      <p
        ref="el"
        :style="text"
        class="has-text-centered"
        contenteditable="true"
        @keyup.delete.prevent.stop
        @keyup="liveTyping"
        @focus="isFocus = true"
        @blur="isFocus = false"
      ></p>
    </template>
  </Object>
</template>

<script>
import Object from "./Object.vue";
import MenuContent from "./Avatar/ContextMenu"; // Text should inherit all of avatar behavior
import { useStore } from "vuex";
import { onMounted, ref, watch } from "vue";

export default {
  props: ["text"],
  components: { Object, MenuContent },
  setup: (props) => {
    const el = ref();
    const store = useStore();

    const isFocus = ref(false);

    const liveTyping = () => {
      const content = el.value.innerHTML;
      store.dispatch("stage/shapeObject", {
        ...props.text,
        content,
      });
    };

    onMounted(() => {
      el.value.innerHTML = props.text.content;
    });
    watch(
      () => props.text.content,
      () => {
        if (!isFocus.value) {
          el.value.innerHTML = props.text.content;
        }
      }
    );

    return { el, liveTyping, isFocus };
  },
};
</script>

<style>
p[contenteditable] {
  outline: none;
}
</style>