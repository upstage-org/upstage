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
          <span class="icon is-small">
            <i :class="item.icon" aria-hidden="true"></i>
          </span>
          <span>{{ item.label }}</span>
        </a>
      </li>
    </ul>
  </div>
  <div v-for="item in items" :key="item.key" v-show="tab === item.key">
    <slot :name="item.key"></slot>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
export default {
  props: ["items", "centered"],
  setup: (props) => {
    const tab = ref(props.items[0].key);
    return { tab };
  },
};
</script>

<style>
</style>