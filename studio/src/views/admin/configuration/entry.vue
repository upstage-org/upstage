<script setup lang="ts">
import { useLoading } from "hooks/mutations";
import { configClient } from "services/graphql";
import { VNode } from "vue";
import { ref } from "vue";

const props = defineProps<{
  name: string;
  label: string;
  defaultValue: string | boolean;
  multiline?: boolean;
  help?: VNode;
}>();

const editing = ref(false);
const value = ref(props.defaultValue);

const { loading, proceed } = useLoading(
  () =>
    configClient.mutation({
      saveConfig: {
        __args: {
          name: props.name,
          value: !value.value ? "" : String(value.value),
        },
        success: true,
      },
    }),
  {
    loading: "Saving config...",
    success: () => "Config saved successfully!",
  }
);

const save = async () => {
  editing.value = false;
  await proceed();
};
</script>

<template>
  <a-form-item
    :label="props.label"
    :name="name"
    :label-col="{ span: 12, xl: { span: 4 }, xxl: { span: 3 } }"
  >
    <template v-if="typeof value === 'string'">
      <a-input-group compact style="display: flex">
        <a-textarea
          v-if="props.multiline"
          :disabled="!editing"
          v-model:value="value"
          style="color: black"
          auto-size
        ></a-textarea>
        <a-input
          v-else
          :disabled="!editing"
          v-model:value="value"
          style="color: black"
        />
        <a-button
          v-if="!editing && !loading"
          type="primary"
          @click="editing = true"
          >Edit</a-button
        >
        <a-button v-else type="primary" @click="save" :loading="loading"
          >Save</a-button
        >
      </a-input-group>
    </template>

    <a-switch
      v-if="typeof value === 'boolean'"
      v-model:checked="value"
      @change="save"
      :loading="loading"
    />
    <help v-if="help" class="mt-2" />
  </a-form-item>
</template>
