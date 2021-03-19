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

    const liveTyping = () => {
      const content = el.value.innerHTML;
      store.dispatch("stage/shapeObject", {
        ...props.text,
        content,
      });
    };

    function setCaretEnd() {
      try {
        const range = document.createRange();
        const sel = window.getSelection();
        const lastNode = el.value.childNodes[el.value.childNodes.length - 1];
        range.setStart(lastNode, lastNode.length);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
      } catch (error) {
        console.log(error);
      }
    }

    onMounted(() => {
      el.value.innerHTML = props.text.content;
    });
    watch(
      () => props.text.content,
      () => {
        el.value.innerHTML = props.text.content;
        setCaretEnd();
      }
    );

    return { el, liveTyping };
  },
};
</script>

<style>
</style>