<template>
  <div class="selectable" :class="{ selected }" @click="$emit('select')">
    <slot></slot>
    <div v-if="revert" class="overlay danger">
      <div class="icon">
        <i class="fas fa-minus"></i>
      </div>
    </div>
    <div v-else class="overlay">
      <div class="icon">
        <i :class="`fas ${multiple && !selected ? 'fa-plus' : 'fa-check'}`"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selected: Boolean,
    revert: Boolean,
    multiple: Boolean,
  },
  emits: ["select"],
};
</script>

<style lang="scss" scoped>

.selectable {
  position: relative;
  cursor: pointer;
  .overlay {
    display: none;
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    border-radius: 5px;
    background-color: rgba($color: #007011, $alpha: 0.5);

    &.danger {
      background-color: rgba($color: #DC5D44, $alpha: 0.5);
    }

    .icon {
      display: flex;
      width: 100%;
      height: 100%;
      color: white;
      font-size: 2rem;
    }
  }
  &:hover,
  &.selected {
    .overlay {
      display: block;
    }
  }
}
</style>
