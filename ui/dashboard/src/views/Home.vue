<template>
  <section id="welcome" class="hero is-fullheight foyer-background">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">CYBERFORMANCE PLATFORM</h1>
        <h2 class="subtitle">
          UpStage is an online venue for live performance: remote performers
          collaborate in real time using digital media, and online audiences
          anywhere in the world join events by going to a web page, without
          having to download and install any additional software. UpStage is
          available free to anyone who would like to use it.
        </h2>
        <Skeleton v-if="loading" />
        <div v-else class="links columns my-4">
          <div class="column">
            <router-link
              v-for="stage in liveStages"
              :key="stage.id"
              :to="`/live/${stage.fileLocation}`"
              class="link my-4"
              :style="backgroundImage(stage.cover, 'live-stage.png')"
            >
              <span>{{ stage.name }}</span>
            </router-link>
          </div>
          <div class="column">
            <router-link
              v-for="stage in upcomingStages"
              :key="stage.id"
              :to="`/live/${stage.fileLocation}`"
              class="link my-4"
              :style="backgroundImage(stage.cover, 'upcoming-performance.png')"
            >
              <span>{{ stage.name }}</span>
            </router-link>
          </div>
          <div class="column">
            <router-link
              to="/live/demo"
              class="link my-4"
              :style="backgroundImage(null, 'latest-news.jpg')"
            >
              <span>Latest News</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import config from "@/../vue.config";
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
import Skeleton from "@/components/Skeleton";
import { absolutePath } from "@/utils/common";

export default {
  name: "Home",
  components: { Skeleton },
  setup: () => {
    const store = useStore();

    const loading = computed(() => store.getters["cache/loadingStages"]);
    const liveStages = computed(() => store.getters["cache/liveStages"]);
    const upcomingStages = computed(
      () => store.getters["cache/upcomingStages"]
    );
    const backgroundImage = (src, defaultSrc) => ({
      "background-image": `url(${
        src ? absolutePath(src) : `${config.publicPath}img/${defaultSrc}`
      })`,
    });

    return {
      backgroundImage,
      liveStages,
      loading,
      upcomingStages,
      absolutePath,
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
    background: white;
    border: 1px solid $black;
    padding: 0.5em;
    max-width: 800px;
    margin: auto;
    box-shadow: 10px 10px 0 0 $primary;
  }
  .column {
    padding: 2rem;
  }
  .link {
    @include textShadow;
    font-weight: bold;
    font-size: 25px;
    border: 1px solid $black;
    border-top: 10px solid $primary;
    display: table;
    width: 100%;
    height: 300px;
    box-shadow: 10px 5px 0 0 $black;
    color: white;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    background-color: white;
    span {
      display: table-cell;
      vertical-align: middle;
    }
  }
}
</style>