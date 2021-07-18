<template>
  <Confirm @confirm="(complete) => duplicateStage(complete)" :loading="loading">
    <Field
      v-model="name"
      label="Enter new stage name"
      :placeholder="defaultName"
    />
    <template #trigger>
      <a class="button is-light is-small" data-tooltip="Duplicate stage">
        <i class="fa fa-lg fa-clone has-text-warning"></i>
      </a>
    </template>

    <template #no>
      <span class="icon">
        <i class="fas fa-times"></i>
      </span>
      <span>Cancel</span>
    </template>
    <template #yes>
      <span class="icon">
        <i class="fas fa-clone"></i>
      </span>
      <span>Duplicate</span>
    </template>
  </Confirm>
</template>

<script>
import { computed, inject, ref } from "vue";
import Confirm from "@/components/Confirm";
import Field from "@/components/form/Field";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { useRouter } from "vue-router";

export default {
  components: { Confirm, Field },
  props: ["stage"],
  setup: (props) => {
    const router = useRouter();
    const name = ref("");
    const defaultName = computed(() => `A clone of ${props.stage.name}`);
    const refresh = inject("refresh");
    const { loading, save } = useMutation(stageGraph.duplicateStage);
    const duplicateStage = async (complete) => {
      const payload = {
        id: props.stage.id,
        name: name.value || defaultName.value,
      };
      const result = await save(
        `${payload.name} was duplicated successfully!`,
        payload
      );
      complete();
      refresh();
      router.push(
        `/backstage/stage-management/${result.duplicateStage.newStageId}/`
      );
      console.log(result);
    };

    return { duplicateStage, name, defaultName, loading };
  },
};
</script>

<style>
</style>