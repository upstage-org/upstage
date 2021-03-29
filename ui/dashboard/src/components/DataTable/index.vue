<template>
  <Skeleton v-if="loading" />
  <div v-else>
    <table class="table">
      <thead>
        <tr>
          <th align="right" v-if="numbered">#</th>
          <th
            v-for="header in headers"
            :key="header"
            align="left"
            :style="{ 'text-align': header.align }"
          >
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
        <transition-group :css="false">
          <tr v-for="(item, index) in rows" :key="item">
            <td align="right" v-if="numbered">{{ offset + index + 1 }}</td>
            <td
              v-for="header in headers"
              :key="header"
              :style="{ 'text-align': header.align }"
              :class="header.slot"
            >
              <slot :name="header.slot" :item="item" :header="header">
                <template v-if="header.render">
                  {{ header.render(item) }}
                </template>
                <template v-else-if="header.type === 'date'">
                  <span :title="moment(item[header.key])">
                    {{ fromNow(item[header.key]) }}
                  </span>
                </template>
                <template v-else>{{ item[header.key] }}</template>
              </slot>
            </td>
          </tr>
        </transition-group>
      </tbody>
    </table>
    <Pagination
      v-model="current"
      v-model:limit="limit"
      :total="totalCount"
      @change="refresh"
    />
  </div>
</template>

<script>
import { useQuery } from "@/services/graphql/composable";
import Skeleton from "@/components/Skeleton";
import { computed } from "@vue/runtime-core";
import moment from "moment";
import Pagination from "./Pagination.vue";

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
      default: true,
    },
    data: {
      type: Array,
    },
  },
  components: { Skeleton, Pagination },
  setup: (props) => {
    if (props.data) {
      return {
        nodes: computed(() => props.data),
        totalCount: computed(() => props.data.length),
      };
    }
    const { nodes, loading, totalCount } = useQuery(props.query);

    return { loading, nodes, totalCount };
  },
  data: function () {
    return {
      current: 1,
      limit: 10,
      now: new Date(),
    };
  },
  methods: {
    moment,
    fromNow(date) {
      return moment(date)
        .subtract(this.now.getTimezoneOffset(), "minute")
        .fromNow();
    },
  },
  computed: {
    offset() {
      return this.limit * (this.current - 1);
    },
    rows() {
      const start = this.offset;
      const end = start + this.limit;
      return this.nodes.slice(start, end);
    },
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
table {
  width: 100%;
}
</style>