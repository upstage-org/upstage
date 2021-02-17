<template>
  <div @click="createText">
    <div class="icon is-large">
      <i class="fas fa-plus fa-2x"></i>
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
  <div class="text-tool" style="width: 200px">
    <span class="tag is-block">Font</span>
    <Dropdown v-model="options.fontFamily" :data="fontFamilies" />
  </div>
  <div class="text-tool">
    <span class="tag is-block">Size</span>
    <Dropdown v-model="options.fontSize" :data="fontSizes" />
  </div>
  <div class="text-tool">
    <span class="tag is-block">Color</span>
    <Dropdown v-model="options.fontSize" :data="fontSizes" />
  </div>
</template>

<script>
import Dropdown from "@/components/form/Dropdown";
import { useStore } from "vuex";
import { computed } from "vue";
export default {
  components: { Dropdown },
  setup: () => {
    const store = useStore();
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
      store.dispatch("stage/openSettingPopup", {
        type: "CreateText",
      });
    };

    return { options, fontSizes, fontFamilies, createText };
  },
};
</script>

<style lang="scss">
.text-tool {
  z-index: 50;
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