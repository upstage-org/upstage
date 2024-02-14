<template>
  <Loading v-if="loading" />
  <div :class="{ 'table-wrapper': wrapper }" v-else>
    <table class="table">
      <thead>
        <tr>
          <th align="right" v-if="numbered">#</th>
          <th
            v-for="header in headers"
            :key="header"
            align="left"
            :style="{ 'text-align': header.align }"
            class="clickable"
            @click="sort(header)"
          >
            <abbr class="has-tooltip-bottom" :data-tooltip="header.description">
              {{ header.title }}
            </abbr>
            &nbsp;
            <template v-if="sortBy?.title === header.title">
              <i
                v-if="header.type === 'date'"
                :class="`fas ${
                  sortOrder ? 'fa-sort-amount-down' : 'fa-sort-amount-down-alt'
                }`"
              />
              <i
                v-else
                :class="`fas ${
                  sortOrder ? 'fa-sort-alpha-down' : 'fa-sort-alpha-down-alt'
                }`"
              />
            </template>
            <template v-else-if="header.sortable">
              <i class="fas fa-sort" />
            </template>
          </th>
        </tr>
      </thead>
      <tfoot v-if="!nodes.length">
        <tr>
          <td
            class="has-text-centered has-text-dark"
            :colspan="headers.length + numbered"
          >
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
              <slot
                :name="header.slot"
                :item="item"
                :header="header"
                :refresh="refresh ?? (() => {})"
              >
                <template v-if="header.render">
                  {{ header.render(item) }}
                </template>
                <template v-else-if="header.type === 'date'">
                  <span :title="moment(item[header.key])">
                    {{ handleFormatDate(item[header.key]) }}
                  </span>
                </template>
                <template v-else>{{ item[header.key] }}</template>
              </slot>
            </td>
          </tr>
        </transition-group>
      </tbody>
    </table>
    <Pagination v-model="current" v-model:limit="limit" :total="totalCount" />
  </div>
</template>

<script>
import { useQuery } from "@/services/graphql/composable";
import Loading from "@/components/Loading";
import { computed } from "vue";
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
    wrapper: {
      type: Boolean,
      default: true,
    },
  },
  components: { Loading, Pagination },
  setup: (props) => {
    if (props.data) {
      return {
        nodes: computed(() => props.data),
        totalCount: computed(() => props.data.length),
      };
    }
    const { nodes, loading, totalCount, refresh } = useQuery(props.query);

    return { loading, nodes, totalCount, refresh };
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
  mounted() {
    const header = this.headers.find((h) => h.defaultSortOrder !== undefined);
    if (header) {
      this.sortBy = header;
      this.sortOrder = header.defaultSortOrder;
    }
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

    handleFormatDate(date) {
      if (date == null) {
        return null;
      }

      if (moment(this.now).diff(date, "weeks") > 1) {
        return moment(date).format("DD/MM/yyyy");
      }

      return this.fromNow(date);
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
            return a[key]?.localeCompare(b[key]);
          }
        });
      }
      if (!this.sortOrder) {
        rows.reverse();
      }
      const start = this.offset;
      const end = start + this.limit;
      let endR;
      if (rows.length < end) {
        endR = rows.length;
      } else {
        endR = end;
      }
      rows?.forEach((row, index) => {
        if (index == endR - 1 || index == endR - 2) {
          row.lastItem = true;
        } else {
          row.lastItem = false;
        }
      });
      return rows.slice(start, end);
    },
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
.table-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
  padding-right: 24px;
}
table {
  width: 100%;
}
</style>
