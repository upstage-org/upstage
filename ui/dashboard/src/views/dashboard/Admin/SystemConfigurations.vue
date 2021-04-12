<template>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>Terms of Service</b>
    </div>
    <template v-if="edit == 'tos'">
      <div class="column"><Field v-model="termsOfService" /></div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="saveToS" :loading="loading">
          Save
        </button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ termsOfService }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'tos'">Edit</button>
      </div>
    </template>
  </div>
</template>

<script>
import Field from "@/components/form/Field";
import { useStore } from "vuex";
import { ref, watchEffect } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { configGraph } from "@/services/graphql";
export default {
  components: { Field },
  setup: () => {
    const store = useStore();
    const termsOfService = ref();
    watchEffect(() => {
      termsOfService.value = store.getters["config/termsOfService"];
    });
    const edit = ref();

    const { loading, save } = useMutation(configGraph.updateTermsOfService);
    const saveToS = () => {
      save("Terms of Services updated successfully!", {
        url: termsOfService.value,
      });
    };

    return { termsOfService, edit, saveToS, loading };
  },
};
</script>

<style>
</style>