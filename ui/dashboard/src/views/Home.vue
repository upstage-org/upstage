<template>
  <section id="welcome" class="hero is-fullheight foyer-background">
    <div class="hero-body">
      <div class="container">
        <div class="describe">
          <h1 class="title" v-html="foyer.title" />
          <h2 v-if="foyer.description" class="subtitle" v-html="foyer.description" />
        </div>
        <Loading v-if="loading" />
        <div v-else class="stages my-4 pt-6">
          <Entry v-for="stage in visibleStages" :key="stage.id" :stage="stage"
            :fallback-cover="stage.status === 'live' ? 'live-stage.png' : 'upcoming-performance.png'" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
import Loading from "@/components/Loading";
import { absolutePath } from "@/utils/common";
import Entry from "@/components/stage/Entry.vue";

export default {
  name: "Home",
  components: { Loading, Entry },
  setup: () => {
    const store = useStore();

    const loading = computed(() => store.getters["cache/loadingStages"]);
    const visibleStages = computed(() => store.getters["cache/visibleStages"]);
    const foyer = computed(() => store.getters["config/foyer"]);

    return {
      visibleStages,
      loading,
      absolutePath,
      foyer,
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

#welcome {
  text-align: center;

  .title {
    @include textShadow;
    font-size: 50px;
  }

  .subtitle {
    padding: 0.5em;
    max-width: 800px;
    margin: auto;
    white-space: pre-wrap;
  }

  .stages {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: masonry;
  }

  .describe {
    position: relative;

    ::after {
      content: '';
      pointer-events: none;
      position: absolute;
      width: 100%;
      height: 100%;
      background-image: url("/img/foyer-background.png");
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      animation: fadeIn 1s;
      opacity: 0.5;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 0.5;
  }
}
</style>