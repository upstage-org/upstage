<template>
  <span @click="openModal">
    <slot name="trigger" />
  </span>
  <div class="modal" :class="{ 'is-active': isActive }">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-card" style="width: 80%">
      <header class="modal-card-head">
        <p class="modal-card-title"><slot name="header" /></p>
        <button class="delete" aria-label="close" @click="closeModal"></button>
      </header>
      <section class="modal-card-body"><slot name="content" /></section>
      <footer class="modal-card-foot">
        <slot name="footer" />
      </footer>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  props: ["active"],
  setup: (props) => {
    const isActive = ref(props.active);

    const openModal = () => (isActive.value = true);
    const closeModal = () => (isActive.value = false);

    return { isActive, openModal, closeModal };
  },
};
</script>

<style>
</style>