<template>
  <div class="columns">
    <div class="column" align="right">
      <template v-if="stage.id">
        <button
          class="button ml-2 is-primary"
          :class="{ 'is-loading': loading }"
          @click="updateStage"
          :disabled="!urlValid"
        >
          {{ $t("save_stage") }}
        </button>
        <ClearChat />
        <SweepStage />
        <DuplicateStage :stage="stage">
          <button class="button ml-2 is-primary">{{ $t("duplicate") }}</button>
        </DuplicateStage>
        <DeleteStage :stage="stage" :refresh="afterDelete">
          <button class="button ml-2 is-danger">
            {{ $t("delete_stage") }}
          </button>
        </DeleteStage>
      </template>
      <template v-else>
        <button
          class="button ml-2 is-primary"
          :class="{ 'is-loading': loading }"
          @click="createStage"
          :disabled="!urlValid"
        >
          {{ $t("create_stage") }}
        </button>
      </template>
    </div>
  </div>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">{{ $t("stage_name") }}</label>
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
          placeholder="URL"
          v-model="form.fileLocation"
          requiredMessage="URL is required"
          expanded
          @keyup="urlValid = null"
          @input="checkURL"
          :right="
            validatingURL
              ? 'fas fa-circle-notch fa-spin'
              : urlValid === true
              ? 'fas fa-check'
              : urlValid === false
              ? 'fas fa-times'
              : 'fas'
          "
          :help="
            !form.fileLocation &&
            `URL must be unique and can't be changed! Please avoid typos, unnecessarily long urls, spaces and punctuation inside URL.`
          "
          :error="urlError"
          :disabled="!!stage.id"
          class="half-flex"
          maxlength="20"
        />
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">{{ $t("description") }}</label>
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

    <div class="field is-horizontal" v-if="stage">
      <div class="field-label">
        <label class="label">{{ $t("status") }}</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <Switch
            :data-tooltip="form.status === 'live' ? 'Live' : 'Rehearsal'"
            :model-value="form.status === 'live'"
            @update:model-value="form.status = $event ? 'live' : 'rehearsal'"
          />
        </div>
        <p class="help">
          The public can only enter your stage when its status is Live. With
          Rehearsal status, only players who have access to the stage can enter.
        </p>
      </div>
    </div>

    <div class="field is-horizontal" v-if="stage">
      <div class="field-label">
        <label class="label">{{ $t("visibility") }}</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <Switch
            :data-tooltip="form.visibility ? 'On' : 'Off'"
            v-model="form.visibility"
          />
        </div>
        <p class="help">
          Select whether this Stage is visible in the Foyer or not.
        </p>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">{{ $t("player_access") }}</label>
        <p class="help">
          Click on a player's name to move them to the column to the right. Use
          a right-click to move them back to the left.
        </p>
      </div>
      <div class="field-body" style="flex-wrap: wrap">
        <MultiTransferAccessColumn
          :columns="[
            'Audience access only',
            'Player access',
            'Player and edit access',
          ]"
          :data="users"
          :owner="owner"
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

    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">{{ $t("cover_image") }}</label>
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
import { inject, reactive, ref, watch, computed, provide } from "vue";
import Field from "@/components/form/Field";
import ImagePicker from "@/components/form/ImagePicker";
import MultiTransferAccessColumn from "@/components/MultiTransferAccessColumn.vue";
import { notification } from "@/utils/notification";
import { useRouter } from "vue-router";
import { displayName } from "@/utils/auth";
import { debounce } from "@/utils/common";
import ClearChat from "./ClearChat";
import SweepStage from "./SweepStage";
import DuplicateStage from "@/components/stage/DuplicateStage";
import DeleteStage from "@/components/stage/DeleteStage";
import { useStore } from "vuex";
import Switch from "@/components/form/Switch.vue";

export default {
  components: {
    Field,
    ClearChat,
    SweepStage,
    MultiTransferAccessColumn,
    ImagePicker,
    DuplicateStage,
    DeleteStage,
    Switch,
  },
  setup: () => {
    const store = useStore();
    const router = useRouter();
    const stage = inject("stage");
    const clearCache = inject("clearCache");

    const form = reactive({
      fileLocation: "",
      ...stage.value,
      ownerId: stage.value.owner?.id,
      status: useAttribute(stage, "status").value ?? "rehearsal",
      visibility: useAttribute(stage, "visibility").value,
      cover: useAttribute(stage, "cover").value,
    });

    const playerAccess = ref(
      useAttribute(stage, "playerAccess", true).value ?? []
    );

    watch(playerAccess, (val) => {
      form.playerAccess = JSON.stringify(val);
    });

    const { nodes } = useQuery(userGraph.userList);
    const users = computed(() =>
      nodes.value
        ? nodes.value.filter((u) => {
            if (stage.value && stage.value.owner) {
              return u.username !== stage.value.owner.username;
            }
            return u.username !== store.state.user.user.username;
          })
        : []
    );

    const owner = computed(() =>
      nodes.value
        ? nodes.value.find((u) => {
            if (stage.value && stage.value.owner) {
              return u.username === stage.value.owner.username;
            }
            return u.username === store.state.user.user.username;
          })
        : []
    );

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
        store.commit("cache/UPDATE_STAGE_VISIBILITY", {
          stageId: form.id,
          visibility: form.visibility,
        });
        console.log(clearCache);
        clearCache();
      } catch (error) {
        notification.error(error);
      }
    };

    const preservedPaths = [
      "backstage",
      "login",
      "register",
      "static",
      "studio",
      "replay",
      "api",
    ];
    const urlValid = ref(!!stage.value.id);
    const { loading: validatingURL, fetch } = useRequest(stageGraph.stageList);

    const validRegex = /^[a-zA-Z0-9-_]*$/;
    const checkURL = debounce(async () => {
      const url = form.fileLocation.trim();
      if (!url || !validRegex.test(url) || preservedPaths.includes(url)) {
        urlValid.value = false;
        return;
      }
      const response = await fetch({
        fileLocation: url,
      });
      urlValid.value = true;
      if (response.stageList.edges.length) {
        const existingStage = response.stageList.edges[0].node;
        if (existingStage.fileLocation !== stage.value.fileLocation) {
          urlValid.value = false;
        }
      }
    }, 500);

    const urlError = computed(() => {
      if (!validRegex.test(form.fileLocation)) {
        return "URL cannot contain special characters or spaces!";
      }
      if (preservedPaths.includes(form.fileLocation.trim())) {
        return `These URL are not allowed: ${preservedPaths.join(", ")}`;
      }
      if (!urlValid.value && form.fileLocation) {
        return "This URL already existed!";
      }
      return null;
    });

    const afterDelete = () => {
      store.dispatch("cache/fetchStages");
      router.push("/backstage/stages");
    };

    const afterDuplicate = () => {
      store.dispatch("cache/fetchStages");
    };

    provide("afterDuplicate", afterDuplicate);

    return {
      form,
      stage,
      createStage,
      updateStage,
      loading,
      users,
      owner,
      displayName,
      checkURL,
      validatingURL,
      urlValid,
      playerAccess,
      afterDelete,
      urlError,
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
