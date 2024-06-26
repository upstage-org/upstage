<template>
  <div v-if="saved">
    <router-link :to="`/replay/${stage.fileLocation}/${saved.id}`" class="button is-small is-light is-success">
      <span class="icon is-small">
        <i class="fas fa-play"></i>
      </span>
      <span>{{ saved.name }}</span>
    </router-link>
  </div>
  <div v-else-if="stage.activeRecording" class="field has-addons">
    <p class="control">
      <a-tooltip title="Stop recording">
        <button @click="saveRecording" class="button is-small is-light is-danger">
          <Loading v-if="saving" height="24px" />
          <span v-else class="icon is-small">
            <i class="fas fa-stop"></i>
          </span>
          <span>{{ label }}</span>
        </button>
      </a-tooltip>
    </p>
    <p class="control">
      <CustomConfirm @confirm="(complete) => deleteRecording(complete)" :loading="deleting">
        <template #trigger>
          <button class="button is-small is-light is-dark">
            <span class="icon is-small">
              <Icon src="delete.svg" />
            </span>
          </button>
        </template>
        <div class="has-text-centered">
          Are you sure you want to delete this recording without saving?
        </div>
      </CustomConfirm>
    </p>
  </div>
  <template v-else>
    <CustomConfirm @confirm="(complete) => startRecording(complete)" :loading="loading">
      <Field v-model="form.name" label="Name" placeholder="Give your recording a name" required />
      <p>
        <i class="fas fa-exclamation-triangle has-text-warning"></i>
        By starting a recording, you acknowledge that the stage
        <span class="has-text-danger">will be cleared!</span> You might wish to
        save your scene before proceed.
      </p>
      <template #no>{{ $t("cancel") }}</template>
      <template #yes>
        <span class="mr-2">
          <i class="fas fa-video"></i>
        </span>
        <span>{{ $t("start_recording") }}</span>
      </template>
      <template #trigger>
        <a-tooltip title="Start recording">
          <button class="button is-light is-small">
            <i class="fas fa-video has-text-primary"></i>
          </button>
        </a-tooltip>
      </template>
    </CustomConfirm>
    <a-tooltip title="View recordings">
      <router-link :to="`/stage-management/${stage.id}/archive`" class="button is-small is-light is-success">
        <span class="icon is-small">
          <i class="fas fa-list"></i>
        </span>
      </router-link>
    </a-tooltip>
  </template>
</template>

<script>
import CustomConfirm from "components/CustomConfirm.vue";
import Loading from "components/Loading.vue";
import Field from "components/form/Field.vue";
import { reactive, ref } from "vue";
import { useMutation } from "services/graphql/composable";
import { stageGraph } from "services/graphql";
import Icon from "components/Icon.vue";
import { computed } from "vue";
import humanizeDuration from "humanize-duration";
import moment from "moment";
import { useStore } from "vuex";
import { notification } from "utils/notification";
import { useClearStage } from "./composable";

export default {
  components: { Confirm, Field, Icon, Loading },
  props: ["stage"],
  setup: (props) => {
    const store = useStore();
    const refresh = () => store.dispatch("cache/fetchStages");

    const form = reactive({
      name: "",
    });

    const clearStage = useClearStage(props.stage.fileLocation);

    const loading = ref(false);
    const { save } = useMutation(stageGraph.startRecording);
    const startRecording = async (complete) => {
      loading.value = true;
      await clearStage();
      await save("Recording started!", props.stage.id, form.name);
      refresh();
      complete();
      loading.value = false;
    };

    const now = ref(moment());
    const interval = setInterval(() => (now.value = moment()), 1000);

    const label = computed(() => {
      const recording = props.stage.activeRecording;
      if (recording) {
        const name = recording.name;
        const from = moment.utc(recording.createdOn);
        const duration = humanizeDuration(
          now.value.diff(from, "milliseconds"),
          {
            round: true,
          },
        );
        return `${name} - ${duration}`;
      }
      return "";
    });

    const { loading: deleting, save: deleteMutation } = useMutation(
      stageGraph.deletePerformance,
    );
    const deleteRecording = async (complete) => {
      await deleteMutation(
        "Recording deleted successfully!",
        props.stage.activeRecording.id,
      );
      Object.assign(props.stage, {
        activeRecording: null,
      });
      refresh();
      complete();
    };

    const saved = ref(false);
    const { loading: saving, save: saveMutation } = useMutation(
      stageGraph.saveRecording,
    );
    const saveRecording = async () => {
      await saveMutation(() => {
        notification.success("Recording saved successfully!");
        saved.value = props.stage.activeRecording;
        clearInterval(interval);
        Object.assign(props.stage, {
          activeRecording: null,
        });
      }, props.stage.activeRecording.id);
    };

    return {
      form,
      startRecording,
      loading,
      label,
      deleteRecording,
      deleting,
      saveRecording,
      saving,
      saved,
    };
  },
};
</script>

<style scoped>
.has-addons {
  justify-content: center !important;
}
</style>
