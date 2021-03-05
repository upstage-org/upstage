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
    <tfoot>
      <tr></tr>
    </tfoot>
    <tbody>
      <tr v-for="(item, index) in nodes" :key="item">
        <td v-if="numbered">{{ index + 1 }}</td>
        <td
          v-for="header in headers"
          :key="header"
          :style="{ 'text-align': header.align }"
        >
          <slot :name="header.slot" :item="item">
            {{ header.render ? header.render(item) : item[header.key] }}
          </slot>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { useQuery } from "@/services/graphql/composable";
import Skeleton from "@/components/Skeleton";

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
  },
  components: { Skeleton },
  setup: (props) => {
    const { nodes, loading } = useQuery(props.query);
    return { loading, nodes };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>