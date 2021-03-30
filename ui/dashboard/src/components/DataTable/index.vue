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
            <abbr
              :data-tooltip="header.description"
              class="clickable"
              @click="sort(header)"
            >
              {{ header.title }}
            </abbr>
            &nbsp;
            <i
              v-if="sortBy?.title === header.title"
              :class="`fas fa-sort-${sortOrder ? 'up' : 'down'}`"
            />
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
      sortBy: null,
      sortOrder: true,
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
    sort(header) {
      if (header.sortable) {
        if (this.sortBy?.title === header.title) {
          this.sortOrder = !this.sortOrder;
        }
        this.sortBy = header;
      }
    },
  },
  computed: {
    offset() {
      return this.limit * (this.current - 1);
    },
    rows() {
      let rows = [...this.nodes];
      if (this.sortBy) {
        const { sortable, type, render, key } = this.sortBy;
        rows = rows.sort((a, b) => {
          if (typeof sortable === "function") {
            return sortable(a, b);
          }
          if (type === "date") {
            moment(a[key]).diff(b[key]);
          }
          if (render) {
            return render(a).localeCompare(render(b));
          }
          if (key) {
            return a[key].localeCompare(b[key]);
          }
        });
      }
      if (!this.sortOrder) {
        rows.reverse();
      }
      const start = this.offset;
      const end = start + this.limit;
      return rows.slice(start, end);
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