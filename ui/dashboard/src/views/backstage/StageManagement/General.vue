<template>
  <div class="columns">
    <div class="column" align="right">
      <template v-if="stage.id">
        <button
          class="button ml-2 is-primary"
          :class="{ 'is-loading': loading }"
          @click="updateStage"
          :disabled="!shortNameValid"
        >Save Stage</button>
        <ClearChat />
        <SweepStage />
        <button class="button ml-2 is-dark">Hide From Stage List</button>
        <DeleteStage :stage="stage" :refresh="afterDelete">
          <button class="button ml-2 is-danger">Delete Stage</button>
        </DeleteStage>
      </template>
      <template v-else>
        <button
          class="button ml-2 is-primary"
          :class="{ 'is-loading': loading }"
          @click="createStage"
          :disabled="!shortNameValid"
        >Create Stage</button>
      </template>
    </div>
  </div>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Stage Name</label>
      </div>
      <div class="field-body">
        <Field
          placeholder="Full Name"
          v-model="form.name"
          required
          requiredMessage="Stage name is required"
          expanded
          class="half-flex"
        />
        <Field
          required
          placeholder="Short Name"
          v-model="form.fileLocation"
          requiredMessage="Short name is required"
          expanded
          @keyup="shortNameValid = null"
          @input="checkShortName"
          :right="
            validatingShortName
              ? 'fas fa-circle-notch fa-spin'
              : shortNameValid === true
                ? 'fas fa-check'
                : shortNameValid === false
                  ? 'fas fa-times'
                  : 'fas'
          "
          :help="!form.fileLocation && `Shortname must be unique and can't be changed! Please watch out for typos, unnecessarily long urls, spaces and punctuations inside shortname.`"
          :error="shortNameError"
          :disabled="!!stage.id"
          class="half-flex"
          maxlength="50"
        />
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Description</label>
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <textarea
              class="textarea"
              placeholder="enter a description (previously only for the splash screen that displays while loading - do we need 2 description fields now, one for the foyer display & one for the splash screen?)"
              v-model="form.description"
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Player access</label>
        <p class="help">
          Click on a player's name to move them to the column to the right. Use
          a right-click to move them back to the left.
        </p>
      </div>
      <div class="field-body" style="flex-wrap: wrap">
        <MultiTransferColumn
          :columns="[
            'Audience access only',
            'Player access',
            'Player and edit access',
          ]"
          :data="users"
          :renderLabel="displayName"
          :renderValue="(item) => item.dbId"
          :renderKeywords="
            (item) =>
              `${item.firstName} ${item.lastName} ${item.username} ${item.email} ${item.displayName}`
          "
          v-model="playerAccess"
        />
      </div>
    </div>

    <div class="field is-horizontal" v-if="stage">
      <div class="field-label">
        <label class="label">Stage Status</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <label class="radio">
              <input type="radio" v-model="form.status" value="live" />
              Live
            </label>
            <label class="radio">
              <input type="radio" v-model="form.status" value="upcoming" />
              Upcoming
            </label>
            <label class="radio">
              <input type="radio" v-model="form.status" value="rehearsal" />
              Rehearsal
            </label>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">Cover image</label>
      </div>
      <div class="field-body">
        <ImagePicker v-model="form.cover" />
      </div>
    </div>
  </div>
</template>

<script>
import {
  useAttribute,
  useMutation,
  useQuery,
  useRequest,
} from "@/services/graphql/composable";
import { stageGraph, userGraph } from "@/services/graphql";
import { inject, reactive, ref, watch, computed } from "vue";
import Field from "@/components/form/Field";
import ImagePicker from "@/components/form/ImagePicker";
import MultiTransferColumn from "@/components/MultiTransferColumn";
import { notification } from "@/utils/notification";
import { useRouter } from "vue-router";
import { displayName } from "@/utils/auth";
import { debounce } from "@/utils/common";
import ClearChat from "./ClearChat";
import SweepStage from "./SweepStage";
import DeleteStage from "@/components/stage/DeleteStage";
import { useStore } from "vuex";

export default {
  components: {
    Field,
    ClearChat,
    SweepStage,
    MultiTransferColumn,
    ImagePicker,
    DeleteStage
  },
  setup: () => {
    const store = useStore();
    const router = useRouter();
    const stage = inject("stage");

    const form = reactive({
      fileLocation: '',
      ...stage.value,
      ownerId: stage.value.owner?.id,
      status: useAttribute(stage, "status").value,
      cover: useAttribute(stage, "cover").value,
    });

    const playerAccess = ref(
      useAttribute(stage, "playerAccess", true).value ?? []
    );

    watch(playerAccess, (val) => {
      form.playerAccess = JSON.stringify(val);
    });

    const { nodes: users } = useQuery(userGraph.userList);
    const { loading, mutation } = useMutation(
      stage.value.id ? stageGraph.updateStage : stageGraph.createStage,
      form
    );
    const createStage = async () => {
      try {
        const stage = await mutation();
        notification.success("Stage created successfully! ID: " + stage.id);
        store.dispatch("cache/fetchStages");
        router.push(`/backstage/stage-management/${stage.id}/`);
      } catch (error) {
        notification.error(error);
      }
    };
    const updateStage = async () => {
      try {
        await mutation();
        notification.success("Stage updated successfully!");
      } catch (error) {
        notification.error(error);
      }
    };

    const preservedPaths = ['backstage', 'login', 'register', 'static', 'studio', 'replay', 'api']
    const shortNameValid = ref(!!stage.value.id);
    const { loading: validatingShortName, fetch } = useRequest(
      stageGraph.stageList
    );

    const validRegex = /^[a-zA-Z0-9-_]*$/;
    const checkShortName = debounce(async () => {
      const shortname = form.fileLocation.trim()
      if (!shortname || !validRegex.test(shortname) || preservedPaths.includes(shortname)) {
        shortNameValid.value = false
        return;
      }
      const response = await fetch({
        fileLocation: shortname,
      });
      shortNameValid.value = true;
      if (response.stageList.edges.length) {
        const existingStage = response.stageList.edges[0].node;
        if (existingStage.fileLocation !== stage.value.fileLocation) {
          shortNameValid.value = false;
        }
      }
    }, 500);

    const shortNameError = computed(() => {
      if (!validRegex.test(form.fileLocation)) {
        return "Shortname should not contain special characters or spaces!";
      }
      if (preservedPaths.includes(form.fileLocation.trim())) {
        return `These shortname are not allowed: ${preservedPaths.join(', ')}`
      }
      if (!shortNameValid.value && form.fileLocation) {
        return 'This short name already existed!'
      }
      return null
    })

    const afterDelete = () => {
      store.dispatch("cache/fetchStages");
      router.push("/backstage/stages");
    }

    return {
      form,
      stage,
      createStage,
      updateStage,
      loading,
      users,
      displayName,
      checkShortName,
      validatingShortName,
      shortNameValid,
      playerAccess,
      afterDelete,
      shortNameError
    };
  },
};
</script>

<style scoped>
.half-flex {
  flex: none;
  flex-basis: 50%;
}
</style>