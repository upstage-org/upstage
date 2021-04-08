<template>
  <footer class="footer">
    <div class="content has-text-centered">
      UpStage v4 -
      <span v-if="release">{{ release }}</span>
      <span v-else>Under construction</span>
    </div>
  </footer>
</template>

<script>
export default {
  setup: () => {
    return { release: process.env.VUE_APP_GIT_BRANCH };
  },
};
</script>

<style>
footer.footer {
  clear: both;
  position: relative;
  padding: 1rem;
}
</style>