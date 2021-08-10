<template>
  <div v-if="saved">
    <router-link
      :to="`/replay/${stage.fileLocation}/${saved.id}`"
      class="button is-small is-light is-success"
    >
      <span class="icon is-small">
        <i class="fas fa-play"></i>
      </span>
      <span>{{ saved.name }}</span>
    </router-link>
  </div>
  <div v-else-if="stage.activeRecording" class="field has-addons">
    <p class="control">
      <button @click="saveRecording" class="button is-small is-light is-danger">
        <Loading v-if="saving" height="24px" />
        <span v-else class="icon is-small">
          <i class="fas fa-stop"></i>
        </span>
        <span>{{ label }}</span>
      </button>
    </p>
    <p class="control">
      <Confirm
        @confirm="(complete) => deleteRecording(complete)"
        :loading="deleting"
      >
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
      </Confirm>
    </p>
  </div>
  <template v-else>
    <Confirm
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
        <button class="button is-light is-small" data-tooltip="Start recording">
          <i class="fas fa-video has-text-primary"></i>
        </button>
      </template>
    </Confirm>
    <router-link
      :to="`/backstage/stage-management/${stage.id}/archive`"
      class="button is-small is-light is-success"
      data-tooltip="View recordings"
    >
      <span class="icon is-small">
        <i class="fas fa-list"></i>
      </span>
    </router-link>
  </template>
</template>

<script>
import Confirm from "@/components/Confirm.vue";
import Loading from "@/components/Loading.vue";
import Field from "@/components/form/Field.vue";
import { reactive, ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Icon from "@/components/Icon.vue";
import { computed } from "@vue/runtime-core";
import humanizeDuration from "humanize-duration";
import moment from "moment";
import { useStore } from "vuex";
import { notification } from "@/utils/notification";
export default {
  components: { Confirm, Field, Icon, Loading },
  props: ["stage"],
  setup: (props) => {
    const store = useStore();
    const refresh = () => store.dispatch("cache/fetchStages");

    const form = reactive({
      name: "",
    });

    const { loading, save } = useMutation(stageGraph.startRecording);
    const startRecording = async (complete) => {
      await save("Recording started!", props.stage.id, form.name);
      refresh();
      complete();
    };

    const now = ref(moment());
    const interval = setInterval(() => (now.value = moment()), 1000);

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

    const { loading: deleting, save: deleteMutation } = useMutation(
      stageGraph.deletePerformance
    );
    const deleteRecording = async (complete) => {
      await deleteMutation(
        "Recording deleted successfully!",
        props.stage.activeRecording.id
      );
      Object.assign(props.stage, {
        activeRecording: null,
      });
      refresh();
      complete();
    };

    const saved = ref(false);
    const { loading: saving, save: saveMutation } = useMutation(
      stageGraph.saveRecording
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