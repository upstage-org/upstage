<template>
  <section
    class="hero bg-cover"
    :class="{ 'is-primary is-fullheight': fullscreen }"
  >
    <div class="hero-body">
      <div class="container has-text-centered">
        <div class="column is-6 is-offset-3">
          <h1 class="title is-uppercase">
            <i class="fas fa-tools" /><br />
            Coming Soon
          </h1>
          <h2 class="subtitle">This is page is under construction</h2>
          <div v-if="fullscreen" class="field is-grouped is-grouped-centered">
            <p class="control">
              <a
                @click="back"
                class="button is-white is-outlined is-rounded is-grouped-centered is-ease is-uppercase has-text-weight-bold"
              >
                <i class="fas fa-arrow-left" />&nbsp;Back
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: ["fullscreen"],
  setup: () => {
    const back = () => window.history.back();
    return { back };
  },
};
</script>

<style>
</style>