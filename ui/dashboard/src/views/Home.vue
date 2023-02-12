<template>
  <section id="welcome" class="hero is-fullheight foyer-background">
    <div class="hero-body">
      <div class="container">
        <div class="describe">
          <h1 class="title" v-html="foyer.title" />
          <h2 v-if="foyer.description" class="subtitle" v-html="foyer.description" />
        </div>
        <Loading v-if="loading" />
        <div v-else class="stages my-4 pt-6">
          <div class="filters">
            <div class="filter sort-filter">
              <Dropdown
                :data="orderTitle"
                :render-label="(item) => item.label"
                :render-value="(item) => item.value"
                v-model="filter.sortBy"
              />
            </div>
            <div class="filter search-filter">
              <Field style="display: inline-block; vertical-align: top;" class="is-fullwidth-mobile" v-model="filter.keyword"
                right="fas fa-search" placeholder="Name of stage" />
            </div>
          </div>
          <masonry-wall :items="visibleStages" :ssr-columns="1" :column-width="300" :gap="32">
            <template #default="{ item }">
              <Entry :stage="item"
                :fallback-cover="item.status === 'live' ? 'live-stage.png' : 'upcoming-performance.png'" />
            </template>
          </masonry-wall>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
import { reactive } from "vue";
import Loading from "@/components/Loading";
import { absolutePath } from "@/utils/common";
import { orderTitle } from "@/utils/constants"
import Entry from "@/components/stage/Entry.vue";
import MasonryWall from '@yeger/vue-masonry-wall'
import Dropdown from "@/components/form/Dropdown.vue";
import Field from "@/components/form/Field.vue";
import { includesIgnoreCase } from "@/utils/common";

export default {
  name: "Home",
  components: { Loading, Entry, MasonryWall, Dropdown, Field },
  setup: () => {
    const store = useStore();

    const filter = reactive({
      sortBy: orderTitle[0].value,
      keyword: null
    });
    const loading = computed(() => store.getters["cache/loadingStages"]);
    const visibleStages = computed(() => {
        let res = store.getters["cache/visibleStages"]
        if (!res) {
          return [];
        }
        if (filter.keyword) {
          res = res.filter((item) =>
            includesIgnoreCase(
              `${item.name}`,
              filter.keyword.trim()
            )
          );
        }
        if (filter.sortBy) {
          res = res.sort(filter.sortBy);
        }
        return res;  
      }
    );
    const foyer = computed(() => store.getters["config/foyer"]);

    return {
      visibleStages,
      loading,
      absolutePath,
      foyer,
      filter,
      orderTitle
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

#welcome {
  text-align: center;

  .title {
    @include textShadow;
    font-size: 50px;
  }

  .subtitle {
    padding: 0.5em;
    max-width: 800px;
    margin: auto;
    white-space: pre-wrap;
  }

  .filters {
    display: flex;
    padding: 0.5em;
    .filter{
      justify-content: center;
      padding-right: 0.5em;
    }
  }

  .describe {
    position: relative;

    ::after {
      content: '';
      pointer-events: none;
      position: absolute;
      width: 100%;
      height: 100%;
      background-image: url("/img/foyer-background.png");
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      animation: fadeIn 1s;
      opacity: 0.5;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 0.5;
  }
}
</style>