<template>
  <div class="columns">
    <div class="column">
      <div class="box">
        <p v-if="titles" class="title is-5">{{ titles[0] }}</p>
        <Skeleton v-if="loading" />
        <div v-else class="columns is-multiline">
          <div
            class="column item"
            :class="{ selected: modelValue.includes(item) }"
            v-for="item in data"
            :key="item"
            @click="select(item)"
          >
            <slot name="render" :item="item">
              {{ item.name }}
            </slot>
            <div class="overlay">
              <div class="icon">
                <i
                  :class="`fas ${
                    modelValue.includes(item) ? 'fa-check' : 'fa-plus'
                  }`"
                ></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column is-narrow">
      <button class="button is-primary" @click="selectAll">
        <i class="fas fa-angle-double-right"></i>
      </button>
      <br />
      <br />
      <button class="button is-primary" @click="removeAll">
        <i class="fas fa-angle-double-left"></i>
      </button>
    </div>
    <div class="column">
      <div class="box">
        <p v-if="titles" class="title is-5">{{ titles[1] }}</p>
        <Skeleton v-if="loading" />
        <div v-else class="columns is-multiline">
          <div
            class="column item"
            v-for="item in modelValue"
            :key="item"
            @click="remove(item)"
          >
            <slot name="render" :item="item">
              {{ item.name }}
            </slot>
            <div class="overlay danger">
              <div class="icon">
                <i class="fas fa-minus"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Skeleton from "@/components/Skeleton";

export default {
  props: {
    modelValue: {
      type: Array,
      required: true,
    },
    data: Array,
    titles: Array,
    loading: Boolean,
  },
  emits: ["update:modelValue"],
  components: { Skeleton },
  setup: (props, { emit }) => {
    const remove = (item) => {
      emit(
        "update:modelValue",
        props.modelValue.filter((value) => value !== item)
      );
    };

    const select = (item) => {
      if (props.modelValue.includes(item)) {
        remove(item);
      } else {
        emit("update:modelValue", props.modelValue.concat(item));
      }
    };

    const selectAll = () => {
      emit("update:modelValue", props.data);
    };

    const removeAll = () => {
      emit("update:modelValue", []);
    };

    return { select, remove, selectAll, removeAll };
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/bulma";

.item {
  position: relative;
  height: fit-content;
  cursor: pointer;

  .overlay {
    display: none;
    position: absolute;
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    top: 10px;
    left: 10px;
    background-color: rgba($color: $primary, $alpha: 0.5);

    &.danger {
      background-color: rgba($color: $danger, $alpha: 0.5);
    }

    .icon {
      display: flex;
      width: 100%;
      height: 100%;
      color: white;
      font-size: 50px;
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