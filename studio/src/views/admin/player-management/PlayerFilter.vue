<script lang="ts">
import { ref, watch, watchEffect, inject, computed, Ref } from "vue";
import { useQuery } from "@vue/apollo-composable";
import { useDebounceFn } from "@vueuse/core";
import gql from "graphql-tag";
import { StudioGraph } from "models/studio";
import { inquiryVar } from "apollo";
import moment, { Moment } from "moment";
import { getSharedAuth } from "utils/common";
import Navbar from "components/Navbar.vue";
import { h } from "vue";
import { Affix, Button, InputSearch, RangePicker, Space } from "ant-design-vue";

export default {
  setup() {
    const { result, loading } = useQuery<StudioGraph>(gql`
      query AdminPlayerFilter {
        adminPlayers {
          edges {
            node {
              id
              username
            }
          }
        }
      }
    `);

    const sharedAuth = getSharedAuth();

    const name = ref("");
    const owners = ref(
      sharedAuth && sharedAuth.username ? [sharedAuth.username] : [],
    );
    const types = ref([]);
    const stages = ref([]);
    const tags = ref([]);
    const dates = ref<[Moment, Moment] | undefined>();

    const ranges = {
      Today: [moment().startOf("day"), moment().endOf("day")],
      Yesterday: [
        moment().subtract(1, "day").startOf("day"),
        moment().subtract(1, "day").endOf("day"),
      ],
      "Last 7 days": [moment().subtract(7, "days"), moment()],
      "This month": [moment().startOf("month"), moment().endOf("day")],
      "Last month": [
        moment().subtract(1, "month").startOf("month"),
        moment().subtract(1, "month").endOf("month"),
      ],
      "This year": [moment().startOf("year"), moment().endOf("day")],
    };

    const updateInquiry = (vars: any) =>
      inquiryVar({
        ...inquiryVar(),
        ...vars,
      });

    const watchInquiryVar = (vars: any) => {
      types.value = vars.mediaTypes ?? [];
      tags.value = vars.tags ?? [];
      console.log(vars);
      inquiryVar.onNextChange(watchInquiryVar);
    };
    inquiryVar.onNextChange(watchInquiryVar);

    watchEffect(() => {
      updateInquiry({
        owners: owners.value,
        stages: stages.value,
        tags: tags.value,
        mediaTypes: types.value,
      });
    });
    watch(
      name,
      useDebounceFn(() => {
        updateInquiry({ name: name.value });
      }, 500),
    );
    watch(dates, (dates) => {
      updateInquiry({
        createdBetween: dates
          ? [
              dates[0].startOf("day").format("YYYY-MM-DD"),
              dates[1].endOf("day").format("YYYY-MM-DD"),
            ]
          : undefined,
      });
    });
    const clearFilters = () => {
      name.value = "";
      owners.value = [];
      types.value = [];
      stages.value = [];
      tags.value = [];
      dates.value = undefined;
    };

    return () =>
      h(Affix, { offsetTop: 0 }, [
        h(
          Space,
          {
            class: "shadow rounded-xl px-4 py-2 bg-white flex justify-between",
          },
          [
            h(
              Space,
              {
                class: "flex-wrap",
              },
              [
                h(InputSearch, {
                  allowClear: true,
                  class: "w-48",
                  placeholder: "Player name",
                  value: name.value,
                  "onUpdate:value": (value: string) => {
                    name.value = value;
                  },
                }),
                h(RangePicker, {
                  placeholder: ["Created from", "to date"],
                  value: dates.value,
                  "onUpdate:value": (value: [Moment, Moment]) => {
                    dates.value = value;
                  },
                  ranges,
                }),
                h(
                  Button,
                  {
                    type: "dashed",
                    onClick: clearFilters,
                  },
                  [
                    h("a-icon", {
                      type: "close-circle",
                    }),
                    "Clear Filters",
                  ],
                ),
              ],
            ),
            h(Navbar),
          ],
        ),
      ]);
  },
};
</script>
