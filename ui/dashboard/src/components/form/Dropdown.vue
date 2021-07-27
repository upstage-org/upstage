<template>
  <div
    class="dropdown"
    :class="{ 'is-active': isActive, 'is-right': isRight, 'is-up': isUp }"
    v-click-outside="() => (isActive = false)"
  >
    <div class="dropdown-trigger">
      <button
        class="button"
        :class="{ 'is-rounded': isRounded }"
        aria-haspopup="true"
        aria-controls="dropdown-menu"
        @click="isActive = !isActive"
      >
        <span v-if="selectedItem">{{ renderLabel(selectedItem) }}</span>
        <span v-else>{{ placeholder }}</span>
        <span class="icon is-small">
          <i class="fas fa-angle-down" aria-hidden="true"></i>
        </span>
      </button>
    </div>
    <div class="dropdown-menu" id="dropdown-menu" role="menu">
      <div
        class="dropdown-content"
        ref="el"
        :style="{ position: fixed ? 'fixed' : 'unset' }"
      >
        <template v-if="data && data.length">
          <a
            v-for="item in data"
            :key="item"
            @click="select(renderValue(item), item)"
            class="dropdown-item"
            :class="{ 'is-active': modelValue === renderValue(item) }"
          >
            <slot name="option" :label="renderLabel(item)" :item="item">
              <div :title="renderDescription(item)" v-if="renderDescription">
                <b>{{ renderLabel(item) }}</b>
                <i class="fas fa-info-circle ml-1"></i>
              </div>
              <template v-else>{{ renderLabel(item) }}</template>
            </slot>
          </a>
        </template>
        <div v-else class="dropdown-item">
          <p class="has-text-dark">No Content</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from "vue";
export default {
  props: {
    data: Array,
    modelValue: String,
    renderLabel: {
      type: Function,
      default: (item) => item,
    },
    renderValue: {
      type: Function,
      default: (item) => item,
    },
    renderDescription: {
      type: Function,
    },
    placeholder: String,
    isRight: Boolean,
    isUp: Boolean,
    isRounded: Boolean,
    fixed: Boolean,
  },
  emits: ["update:modelValue", "select"],
  setup: (props, { emit }) => {
    const selectedItem = computed(() =>
      props.data?.find((item) => props.renderValue(item) === props.modelValue)
    );
    const isActive = ref();
    const select = (value, item) => {
      emit("update:modelValue", value);
      emit("select", value, item);
      isActive.value = false;
    };
    const el = ref();
    const scrollIntoView = () =>
      el.value.querySelector(".is-active")?.scrollIntoView();
    onMounted(scrollIntoView);
    return { select, selectedItem, isActive, el };
  },
};
</script>

<style lang="scss" scoped>
.dropdown-content {
  max-height: 50vh;
  overflow-y: auto;
}
</style>