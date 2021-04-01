<template>
  <nav
    class="pagination is-centered is-rounded"
    role="navigation"
    aria-label="pagination"
  >
    <button
      class="button pagination-previous"
      :disabled="modelValue === 1"
      @click="goToPage(modelValue - 1)"
    >
      Previous page
    </button>
    <button
      class="button pagination-next"
      :disabled="modelValue === totalPages"
      @click="goToPage(modelValue + 1)"
    >
      Next page
    </button>
    <Dropdown
      :data="[5, 10, 25, 50, 100]"
      is-up
      is-right
      is-rounded
      style="order: 3"
      :modelValue="limit"
      @update:modelValue="changeLimit"
      :renderLabel="(value) => `${value} items per page`"
    />
    <ul class="pagination-list">
      <li>
        <a
          class="pagination-link"
          :class="{ 'is-current': modelValue === 1 }"
          @click="goToPage(1)"
          >1</a
        >
      </li>
      <li v-if="visibleNavigationButtons[0] > 2">
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li v-for="page in visibleNavigationButtons" :key="page">
        <a
          class="pagination-link"
          :class="{ 'is-current': page === modelValue }"
          @click="goToPage(page)"
        >
          {{ page }}
        </a>
      </li>
      <li
        v-if="
          visibleNavigationButtons[visibleNavigationButtons.length - 1] <
          totalPages - 1
        "
      >
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li v-if="totalPages > 1">
        <a
          class="pagination-link"
          :class="{ 'is-current': modelValue === totalPages }"
          @click="goToPage(totalPages)"
        >
          {{ totalPages }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
import { computed } from "@vue/runtime-core";
import Dropdown from "@/components/form/Dropdown";
export default {
  props: {
    total: {
      type: Number,
      default: 0,
    },
    modelValue: Number,
    limit: Number,
    maxNavigationButtons: {
      type: Number,
      default: 7,
    },
  },
  components: { Dropdown },
  emits: ["update:modelValue", "update:limit", "page"],
  setup: (props, { emit }) => {
    const goToPage = (page) => {
      emit("update:modelValue", page);
      emit("change");
    };

    const changeLimit = (limit) => {
      emit("update:modelValue", 1);
      emit("update:limit", limit);
      emit("change");
    };

    const totalPages = computed(() => Math.ceil(props.total / props.limit));
    const visibleNavigationButtons = computed(() => {
      const buttons = [];
      let begin = Math.ceil(
        props.modelValue - (props.maxNavigationButtons - 2) / 2
      );
      if (begin < 2) {
        begin = 2;
      }
      let end = begin + props.maxNavigationButtons - 3;
      if (end > totalPages.value - 1) {
        begin = Math.max(2, begin - (end - totalPages.value + 1));
        end = totalPages.value - 1;
      }
      for (let i = begin; i <= end; i++) {
        buttons.push(i);
      }
      return buttons;
    });

    return { goToPage, totalPages, visibleNavigationButtons, changeLimit };
  },
};
</script>

<style>
</style>