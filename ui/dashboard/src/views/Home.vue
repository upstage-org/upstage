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
        <div class="links columns is-vcentered my-4">
          <div class="column">
            <router-link
              to="/live"
              class="link"
              :style="{ 'background-image': url('live-stage.png') }"
            >
              <span>Live Stage</span>
            </router-link>
          </div>
          <div class="column">
            <router-link
              to="/live"
              class="link"
              :style="{ 'background-image': url('upcoming-performance.png') }"
            >
              <span> Upcoming Performance </span>
            </router-link>
          </div>
          <div class="column">
            <router-link
              to="/live"
              class="link"
              :style="{ 'background-image': url('latest-news.jpg') }"
            >
              <span>Ticketing</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import config from "@/../vue.config";

export default {
  name: "Home",
  components: {},
  setup: () => {
    const url = (src) => `url(${config.publicPath}img/${src})`;
    return { url };
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