<template>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>{{ $t("tos.terms_of_service") }}</b>
    </div>
    <template v-if="edit == 'tos'">
      <div class="column">
        <Field v-model="termsOfService" />
      </div>
      <div class="column is-narrow">
        <button class="button is-primary" :class="{ 'is-loading': loadingTOS }" @click="saveToS">{{ $t("save") }}</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ termsOfService }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'tos'">{{ $t("edit") }}</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>{{ $t("manual") }}</b>
    </div>
    <template v-if="edit == 'manual'">
      <div class="column">
        <Field v-model="manual" />
      </div>
      <div class="column is-narrow">
        <button class="button is-primary" :class="{ 'is-loading': loading }" @click="saveManual">{{ $t("save") }}</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ manual }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'manual'">{{ $t("edit") }}</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column is-narrow">
      <b>{{ $t("email_subject_prefix") }}</b>
    </div>
    <template v-if="edit == 'esp'">
      <div class="column">
        <Field v-model="esp" />
      </div>
      <div class="column is-narrow">
        <button class="button is-primary" :class="{ 'is-loading': loading }" @click="saveESP">{{ $t("save") }}</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ esp }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'esp'">{{ $t("edit") }}</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column  is-narrow">
      <b>{{ $t("enable_upstage_donate") }}</b>
    </div>
    <div class="column  is-narrow">
      <Switch v-model="enableDonate"
        @update:model-value="saveConfig(`${enableDonate ? 'Enable' : 'Disable'} donations for Upstage successfully!`, 'ENABLE_DONATE', enableDonate || '')"
        :loading="loading" />
    </div>
  </div>
</template>

<script>
import Field from "@/components/form/Field";
import { useStore } from "vuex";
import { ref, watchEffect } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { configGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import Switch from "@/components/form/Switch.vue";
export default {
  components: { Field, Switch },
  setup: () => {
    const store = useStore();
    const termsOfService = ref();
    watchEffect(() => {
      termsOfService.value = store.getters["config/termsOfService"];
    });
    const edit = ref();

    const { loading: loadingTOS, save } = useMutation(configGraph.updateTermsOfService);
    const saveToS = () => {
      save(() => {
        notification.success("Terms of Services updated successfully!");
        store.dispatch("config/fetchConfig");

      }, {
        url: termsOfService.value,
      });
    };
    const manual = ref();
    watchEffect(() => {
      manual.value = store.getters["config/manual"];
    });
    const { loading, save: saveConfig } = useMutation(configGraph.saveConfig);
    const saveManual = () => {
      saveConfig(() => {
        notification.success("Manual link updated successfully!");
        store.dispatch("config/fetchConfig");
      }, 'MANUAL', manual.value);
    };

    const esp = ref();
    watchEffect(() => {
      esp.value = store.getters["config/esp"];
    });

    const saveESP = () => {
      saveConfig(() => {
        notification.success("Email Subject Prefix updated successfully!")
        store.dispatch("config/fetchConfig");
      }, 'EMAIL_SUBJECT_PREFIX', esp.value);
    };

    const enableDonate = ref(false);
    watchEffect(() => {
      enableDonate.value = store.getters["config/enableDonate"];
    });

    return { termsOfService, edit, saveToS, loadingTOS, manual, saveManual, loading, esp, saveESP, enableDonate, saveConfig };
  },
};
</script>

<style>
</style>
