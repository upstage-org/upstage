<template>
  <Object :object="object">
    <template #menu="slotProps">
      <div class="avatar-context-menu card-content p-0">
        <a class="panel-block has-text-info" @click="slotProps.closeMenu()">
          <span class="panel-icon">
            <i class="fas fa-map-marker-alt has-text-info"></i>
          </span>
          <span>Change Shape</span>
        </a>
      </div>
    </template>
  </Object>
</template>

<script>
import { reactive } from "vue";
import Object from "./Object.vue";
export default {
  components: { Object },
  props: ["stream"],
  setup: (props) => {
    const object = reactive(props.stream);
    object.src = "123";

    return { object };
  },
};
</script>

<style>
</style>