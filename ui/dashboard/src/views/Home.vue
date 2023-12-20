<template>
  <section id="welcome" class="hero is-fullheight foyer-background">
    <div class="hero-body">
      <div class="container">
        <h1 class="title" v-html="foyer.title" />
        <h2 v-if="foyer.description" class="subtitle" v-html="foyer.description" />
        <Loading v-if="loading" />
        <div
          v-else
          class="links columns is-multiline my-4 pt-6"
          data-masonry="{ 'itemSelector': '.column', 'columnWidth': 200 }"
        >
          <div v-for="stage in liveStages" :key="stage.id" class="column is-4">
            <router-link
              :to="`/${stage.fileLocation}`"
              class="link"
              :style="backgroundImage(stage.cover, 'live-stage.png')"
            >
              <PlayerAudienceCounter :stage-url="stage.fileLocation" class="counter" />
              <span>{{ stage.name }}</span>
            </router-link>
          </div>
          <div v-for="stage in upcomingStages" :key="stage.id" class="column is-4">
            <router-link
              :to="`/${stage.fileLocation}`"
              class="link"
              :style="backgroundImage(stage.cover, 'upcoming-performance.png')"
            >
              <span>{{ stage.name }}</span>
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
import Loading from "@/components/Loading";
import { absolutePath } from "@/utils/common";
import PlayerAudienceCounter from "@/components/stage/PlayerAudienceCounter";

export default {
  name: "Home",
  components: { Loading, PlayerAudienceCounter },
  setup: () => {
    const store = useStore();

    const loading = computed(() => store.getters["cache/loadingStages"]);
    const liveStages = computed(() => store.getters["cache/liveStages"]);
    const foyer = computed(() => store.getters["config/foyer"]);
    const upcomingStages = computed(
      () => store.getters["cache/upcomingStages"]
    );
    const backgroundImage = (src, defaultSrc) => ({
      "background-image": `url(${src ? absolutePath(src) : `${config.publicPath}img/${defaultSrc}`
        })`,
    });

    return {
      backgroundImage,
      liveStages,
      loading,
      upcomingStages,
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
    background: white;
    border: 1px solid $black;
    padding: 0.5em;
    max-width: 800px;
    margin: auto;
    box-shadow: 10px 10px 0 0 $primary;
    white-space: pre-wrap;
  }
  .column {
    padding: 2rem;
  }
  .link {
    @include textShadow;
    position: relative;
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
    .counter {
      position: absolute;
      right: 10px;
      top: 10px;
      width: auto !important;
    }
  }
}
</style>