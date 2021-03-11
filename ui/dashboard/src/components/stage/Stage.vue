<template>
  <Modal>
    <template #trigger>
      <article class="tile is-child notification is-light">
        <figure class="image is-4by3">
          <img class="stage-image" src="@/assets/upstage.png" />
        </figure>
        <p class="title has-text-primary">{{ stage.name }}</p>
        <p class="subtitle">
          <span v-if="author">Author: {{ stage.author }}<br /></span>
          <span v-if="access">Your Access: {{ stage.access }}</span>
        </p>
      </article>
    </template>
    <template #header>Stage Detail</template>
    <template #content><Detail :stage="stage" /></template>
    <template #footer><ActionButtons :stage="stage" /></template>
  </Modal>
</template>

<script>
import Modal from "../Modal";
import Detail from "./Detail";
import ActionButtons from "./ActionButtons";

export default {
  components: { Modal, Detail, ActionButtons },
  props: ["stage"],
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