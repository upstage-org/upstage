<script setup lang="ts">
import { ref, watchEffect } from "vue";
import { selectedMenuVar } from "apollo";

const selectedKeys = ref([selectedMenuVar()]);
watchEffect(() => {
  selectedMenuVar(selectedKeys.value[0]);
});
</script>

<template>
  <a-layout-sider collapsed class="bg-transparent">
    <a-menu
      v-model:selectedKeys="selectedKeys"
      mode="inline"
      class="upstage-menu"
    >
      <a-menu-item key="media">
        <picture-outlined />&nbsp;
        <span>Media</span>
      </a-menu-item>
      <a-menu-item key="stage">
        <layout-outlined />
        <span>Stages</span>
      </a-menu-item>
      <a-menu-item key="profile">
        <user-outlined />
        <span>Profile</span>
      </a-menu-item>
      <a-menu-item key="admin">
        <key-outlined />
        <span>Profile</span>
      </a-menu-item>
      <a-menu-item key="manual" href="https://docs.upstage.live/">
        <book-outlined />
        <span>Manual</span>
      </a-menu-item>
    </a-menu>
  </a-layout-sider>
</template>

<style lang="less">
.upstage-menu {
  margin-top: 16px;
  margin-left: 16px;
  margin-right: 0;
  border-radius: 12px;

  .ant-menu-item {
    margin: 0;
    border-radius: 12px;

    &:active {
      background-color: transparent;
    }

    &.ant-menu-item-selected {
      background-color: #147d20;
      color: white;
    }
  }
}

.ant-tooltip-inner {
  [role="img"].anticon {
    margin-right: 8px;
  }
}
</style>
