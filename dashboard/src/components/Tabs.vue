<template>
  <div class="tabs is-boxed" :class="{ 'is-centered': centered }">
    <ul>
      <li
        v-for="item in items"
        :key="item.key"
        :class="{ 'is-active': tab === item.key }"
        @click="tab = item.key"
      >
        <a>
          <span v-if="item.icon" class="icon is-small">
            <i :class="item.icon" aria-hidden="true"></i>
          </span>
          <span>{{ item.label }}</span>
        </a>
      </li>
      <slot name="extras"></slot>
    </ul>
  </div>
  <div class="tab-content">
    <div :class="`tab-${item.key}`" v-for="item in items" :key="item.key">
      <template v-if="tab === item.key">
        <slot :name="item.key"></slot>
      </template>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  props: ["items", "centered"],
  setup: (props) => {
    const tab = ref(props.items[0].key);
    return { tab };
  },
};
</script>

<style>
.tabs {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 10;
}
</style>
