<template>
  <article
    class="tile is-child notification is-light"
    @click="() => (showDetail = true)"
  >
    <figure class="image is-4by3">
      <img class="stage-image" src="@/assets/upstage.png" />
    </figure>
    <p class="title has-text-primary">{{ name }}</p>
    <p class="subtitle">
      <span v-if="author">Author: {{ author }}<br /></span>
      <span v-if="access">Your Access: {{ access }}</span>
    </p>
  </article>
  <div class="modal" :class="{ 'is-active': showDetail }">
    <div class="modal-background" @click="closeDetail"></div>
    <div class="modal-card" style="width: 80%">
      <header class="modal-card-head">
        <p class="modal-card-title">Stage Detail</p>
        <button class="delete" aria-label="close" @click="closeDetail"></button>
      </header>
      <section class="modal-card-body"><Detail :name="name" /></section>
      <footer class="modal-card-foot">
        <DuplicateButton />
      </footer>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import Detail from "./Detail";
import DuplicateButton from "./DuplicateButton";

export default {
  components: { Detail, DuplicateButton },
  props: ["name", "author", "access"],
  setup: () => {
    const showDetail = ref(false);

    const closeDetail = () => (showDetail.value = false);

    return { showDetail, closeDetail };
  },
};
</script>

<style scoped>
.stage-image {
  height: auto !important;
  margin: auto;
}
.title {
  font-size: 24px;
}
article {
  cursor: pointer;
}
</style>