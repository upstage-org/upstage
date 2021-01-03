<template>
  <section class="hero is-medium is-primary is-bold">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">WHAT’S ON</h1>
        <h2 class="subtitle">
          <ul>
            <li>List of live & soon-live public performances</li>
            <li>Title, thumbnail image, brief description, more info link</li>
            <li>Live link at show-time</li>
          </ul>
        </h2>
        <h2 class="subtitle">
          <router-link
            to="/live"
            class="button is-large is-rounded is-outlined is-white"
          >
            <span class="icon is-medium">
              <i class="fas fa-play"></i>
            </span>
            <span>Demo Stage</span>
          </router-link>
        </h2>
      </div>
    </div>
  </section>
  <section class="hero is-medium is-dark is-bold">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">BOX OFFICE</h1>
        <h2 class="subtitle">
          <ul>
            <li>Buy tickets – link to 3rd party platform eg Eventbrite etc.</li>
          </ul>
        </h2>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Home",
  components: {},
};
</script>
