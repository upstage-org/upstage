<template>
  <Modal>
    <template #trigger>
      <article class="tile is-child notification is-light">
        <figure class="image is-4by3">
          <img class="stage-image" src="@/assets/upstage.png" />
        </figure>
        <p class="title has-text-primary">{{ name }}</p>
        <p class="subtitle">
          <span v-if="author">Author: {{ author }}<br /></span>
          <span v-if="access">Your Access: {{ access }}</span>
        </p>
      </article>
    </template>
    <template #header>Stage Detail</template>
    <template #content><Detail :name="name" /></template>
    <template #footer><DuplicateButton /></template>
  </Modal>
</template>

<script>
import Modal from "../Modal";
import Detail from "./Detail";
import DuplicateButton from "./DuplicateButton";

export default {
  components: { Modal, Detail, DuplicateButton },
  props: ["name", "author", "access"],
  setup: () => {},
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