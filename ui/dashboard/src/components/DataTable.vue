<template>
  <table class="table" :class="{ 'is-loading': loading }">
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
        <td v-for="header in headers" :key="header">
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