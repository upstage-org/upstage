<template>
  <div class="tile is-ancestor">
    <div class="tile is-parent is-6">
      <article class="tile is-child notification is-white">
        <div class="content">
          <img class="stage-image" src="@/assets/upstage.png" />
          <p class="title">{{ stage.name }}</p>
          <p class="subtitle">
            Statistique max
            <span>
              18
              <span class="icon has-text-dark">
                <i class="fas fa-desktop"></i>
              </span>
            </span>

            <span>
              5
              <span class="icon has-text-dark">
                <i class="fas fa-mobile"></i>
              </span>
            </span>
          </p>
          <p class="subtitle">
            <a href="#" class="has-text-info">Recorded link</a>
          </p>
        </div>
      </article>
    </div>
    <div class="tile is-parent is-6">
      <article class="tile is-child notification is-white">
        <div class="content">
          <div class="content">
            <strong v-if="stage.description">{{ stage.description }}</strong>
            <span v-for="i in [1, 2, 3, 4, 5]" :key="i">
              <br />
              <span class="icon has-text-dark">
                <i class="fas fa-user"></i>
              </span>
              Name player artists
            </span>
          </div>
          <div class="content">
            <span> Scene: x files </span><br />
            <span> Avatar: x files </span><br />
            <span> Props: x files </span><br />
            <span> Backdrop: x files </span><br />
            <span> Sound: x files </span><br />
            <span> Video: x files </span><br />
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
export default {
  props: ["stage"],
};
</script>

<style scoped>
</style>