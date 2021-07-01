<template>
  <Object :object="object">
    <template #menu="slotProps">
      <MenuContent
        :object="object"
        v-bind="slotProps"
        v-model:active="active"
      />
    </template>
    <template #render>
      <p
        ref="el"
        :style="object"
        class="has-text-centered show-text"
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
  props: ["object"],
  components: { Object, MenuContent },
  setup: (props) => {
    const el = ref();
    const store = useStore();

    const isFocus = ref(false);

    const liveTyping = () => {
      const content = el.value.innerHTML;
      store.dispatch("stage/shapeObject", {
        ...props.object,
        content,
      });
    };

    onMounted(() => {
      el.value.innerHTML = props.object.content;
    });
    watch(
      () => props.object.content,
      () => {
        if (!isFocus.value) {
          el.value.innerHTML = props.object.content;
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
  pointer-events: all;
}
.show-text {
  white-space: nowrap;
  cursor: text;
}
</style>