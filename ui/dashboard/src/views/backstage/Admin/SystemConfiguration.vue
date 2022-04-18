<template>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>Terms of Service</b>
    </div>
    <template v-if="edit == 'tos'">
      <div class="column">
        <Field v-model="termsOfService" />
      </div>
      <div class="column is-narrow">
        <button
          class="button is-primary"
          :class="{ 'is-loading': loadingTOS }"
          @click="saveToS"
        >Save</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ termsOfService }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'tos'">Edit</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>Manual</b>
    </div>
    <template v-if="edit == 'manual'">
      <div class="column">
        <Field v-model="manual" />
      </div>
      <div class="column is-narrow">
        <button
          class="button is-primary"
          :class="{ 'is-loading': loading }"
          @click="saveManual"
        >Save</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ manual }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'manual'">Edit</button>
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

    const { loading: loadingTOS, save } = useMutation(configGraph.updateTermsOfService);
    const saveToS = () => {
      save("Terms of Services updated successfully!", {
        url: termsOfService.value,
      });
    };
    const manual = ref();
    watchEffect(() => {
      manual.value = store.getters["config/manual"];
    });
    const { loading, save: saveConfig } = useMutation(configGraph.saveConfig);
    const saveManual = () => {
      saveConfig("Manual link updated successfully!", 'MANUAL', manual.value);
    };

    return { termsOfService, edit, saveToS, loadingTOS, manual, saveManual, loading };
  },
};
</script>

<style>
</style>
