<template>
  <section v-if="isWriting" class="writing" @click="onClickWriting">
    <p ref="el" :style="options" contenteditable="true">
      Write or paste<br />your text here
    </p>
  </section>
  <div v-if="!isWriting" @click="createText" class="text-tool">
    <div class="icon is-large">
      <i class="fas fa-plus fa-2x"></i>
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
  <template v-else>
    <div class="text-tool">
      <div class="icon is-large">
        <i class="fas fa-check fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Save</span>
    </div>
    <div class="text-tool" @click="cancelWriting">
      <div class="icon is-large">
        <i class="fas fa-times fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Cancel</span>
    </div>
  </template>
  <div class="text-tool" style="width: 200px; z-index: 1005">
    <span class="tag is-block">Font</span>
    <Dropdown v-model="options.fontFamily" :data="fontFamilies" />
  </div>
  <div class="text-tool" style="z-index: 1004">
    <span class="tag is-block">Size</span>
    <Dropdown v-model="options.fontSize" :data="fontSizes" />
  </div>
  <div class="text-tool" style="z-index: 1003">
    <span class="tag is-block">Color</span>
    <ColorPicker v-model="options.color" />
  </div>
</template>

<script>
import Dropdown from "@/components/form/Dropdown";
import ColorPicker from "@/components/form/ColorPicker";
import { useStore } from "vuex";
import { computed, ref } from "vue";
export default {
  components: { Dropdown, ColorPicker },
  setup: () => {
    const store = useStore();
    const isWriting = computed(() => store.state.stage.preferences.isWriting);
    const options = computed(() => store.state.stage.preferences.text);
    let fontSizes = [];
    for (let i = 1; i <= 100; i++) {
      fontSizes.push(`${i}px`);
    }
    const fontFamilies = [
      "Josefin Sans",
      "Arial",
      "Times New Roman",
      "Helvetica",
      "Times",
      "Courier New",
      "Verdana",
      "Courier",
      "Arial Narrow",
      "Candara",
      "Geneva",
      "Calibri",
      "Optima",
      "Cambria",
      "Garamond",
      "Perpetua",
      "Monaco",
      "Didot",
      "Brush Script MT",
      "Lucida Bright",
      "Copperplate",
    ];

    const createText = () => {
      store.commit("stage/UPDATE_IS_WRITING", true);
    };

    const cancelWriting = () => {
      store.commit("stage/UPDATE_IS_WRITING", false);
    };

    const el = ref();
    const onClickWriting = (e) => {
      const { width, height } = el.value.getBoundingClientRect() ?? {};
      store.commit("stage/UPDATE_TEXT_OPTIONS", {
        left: e.clientX - width / 2 + "px",
        top: e.clientY - height / 2 + "px",
      });
      el.value.focus();
    };

    return {
      options,
      fontSizes,
      fontFamilies,
      createText,
      isWriting,
      cancelWriting,
      onClickWriting,
      el,
    };
  },
};
</script>

<style lang="scss">
[contenteditable] {
  -webkit-user-select: text !important;
  user-select: text !important;
}
.writing {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  background-color: rgba($color: white, $alpha: 0.5);
  backdrop-filter: blur(5px);
  > p {
    position: absolute;
  }
}
.text-tool {
  z-index: 1001;
  position: relative;
  float: left;
  .dropdown {
    position: absolute;
    transform: translateX(-50%);
  }
  &:hover {
    .tag {
      background: transparent;
      color: white;
    }
  }
}
</style>