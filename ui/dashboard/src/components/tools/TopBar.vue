<template>
  <div id="topbar" class="card is-light" v-if="tool">
    <div class="card-content">
      <component :is="tool" />
    </div>
  </div>
</template>

<script>
import Avatars from "./Avatars";
import Backdrops from "./Backdrops";
import Props from "./Props";

export default {
  props: ["tool"],
  components: { Avatars, Backdrops, Props },
};
</script>

<style lang="scss" scoped>
#topbar {
  position: fixed;
  max-width: 80vw;
  height: 100px;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.9;
  .card-content {
    overflow-x: auto;
  }
}
</style>