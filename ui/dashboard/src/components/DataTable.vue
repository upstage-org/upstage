<template>
  <Skeleton v-if="loading" />
  <table v-else class="table">
    <thead>
      <tr>
        <th v-if="numbered">#</th>
        <th v-for="header in headers" :key="header">
          <abbr :title="header.description">{{ header.title }}</abbr>
        </th>
      </tr>
    </thead>
    <tfoot v-if="!nodes.length">
      <tr>
        <td class="has-text-centered has-text-dark" :colspan="headers.length">
          <i class="fas fa-frown fa-4x"></i>
          <div>Sorry, no record match your criteria!</div>
        </td>
      </tr>
    </tfoot>
    <tbody>
      <transition-group :css="false" @enter="enter" @leave="leave">
        <tr v-for="(item, index) in nodes" :key="item">
          <td v-if="numbered">{{ index + 1 }}</td>
          <td
            v-for="header in headers"
            :key="header"
            :style="{ 'text-align': header.align }"
            :class="header.slot"
          >
            <slot :name="header.slot" :item="item" :header="header">
              {{ header.render ? header.render(item) : item[header.key] }}
            </slot>
          </td>
        </tr>
      </transition-group>
    </tbody>
  </table>
</template>

<script>
import { useQuery } from "@/services/graphql/composable";
import Skeleton from "@/components/Skeleton";
import { computed } from "@vue/runtime-core";
import anime from "animejs";

export default {
  props: {
    query: {
      type: Function,
    },
    headers: {
      type: Array,
      default: () => [],
    },
    numbered: {
      type: Boolean,
      default: false,
    },
    data: {
      type: Array,
    },
  },
  components: { Skeleton },
  setup: (props) => {
    if (props.data) {
      return { nodes: computed(() => props.data) };
    }
    const { nodes, loading } = useQuery(props.query);

    return { loading, nodes };
  },
  methods: {
    enter(el, complete) {
      anime({
        targets: el,
        translateX: [100, 0],
        complete,
      });
    },
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>