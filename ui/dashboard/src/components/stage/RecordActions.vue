<template>
  <div v-if="stage.activeRecording" class="field has-addons">
    <p class="control">
      <button class="button is-small is-light is-danger">
        <span class="icon is-small">
          <i class="fas fa-stop"></i>
        </span>
        <span>{{ label }}</span>
      </button>
    </p>
    <p class="control">
      <button class="button is-small is-light is-dark">
        <span class="icon is-small">
          <Icon src="delete.svg" />
        </span>
      </button>
    </p>
  </div>
  <Confirm
    v-else
    @confirm="(complete) => startRecording(complete)"
    :loading="loading"
  >
    <Field
      v-model="form.name"
      label="Name"
      placeholder="Give your recording a name"
      required
    />
    <template #no> Cancel </template>
    <template #yes>
      <span class="mr-2">
        <i class="fas fa-video"></i>
      </span>
      <span>Start Recording</span>
    </template>
    <template #trigger>
      <button class="button is-light is-small">
        <i class="fas fa-video has-text-primary"></i>
      </button>
    </template>
  </Confirm>
</template>

<script>
import Confirm from "@/components/Confirm.vue";
import Field from "@/components/form/Field.vue";
import { reactive, ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Icon from "@/components/Icon.vue";
import { computed } from "@vue/runtime-core";
import humanizeDuration from "humanize-duration";
import moment from "moment";
export default {
  components: { Confirm, Field, Icon },
  props: ["stage"],
  setup: (props) => {
    const form = reactive({
      name: "",
    });

    const { loading, save } = useMutation(stageGraph.startRecording);
    const startRecording = async (complete) => {
      await save("Recording started!", props.stage.id, form.name);
      complete();
    };

    const now = ref(moment());
    setInterval(() => (now.value = moment()), 1000);

    const label = computed(() => {
      const recording = props.stage.activeRecording;
      if (recording) {
        const name = recording.name;
        const from = moment.utc(recording.createdOn);
        console.log(from);
        const duration = humanizeDuration(
          now.value.diff(from, "milliseconds"),
          {
            round: true,
          }
        );
        return `${name} - ${duration}`;
      }
    });

    return { form, startRecording, loading, label };
  },
};
</script>

<style scoped>
.has-addons {
  justify-content: center;
}
</style>