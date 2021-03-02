<template>
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
        />
        <Field
          required
          placeholder="Short Name"
          v-model="form.fileLocation"
          requiredMessage="Short name is required"
          right="fas fa-check"
          help="From which the stage URL is created"
          expanded
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
        <label class="label">Users</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select v-model="form.ownerId">
                <option v-for="user in users" :key="user" :value="user.id">
                  {{ displayName(user) }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal" v-if="id">
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
        <!-- Left empty for spacing -->
      </div>
      <div class="field-body">
        <div class="field">
          <div class="control">
            <template v-if="id">
              <button
                class="button mr-2 mt-2 is-primary"
                :class="{ 'is-loading': loading }"
                @click="updateStage"
              >
                Save Stage
              </button>
              <button class="button mr-2 mt-2 is-warning">Clear Chat</button>
              <button class="button mr-2 mt-2 is-warning">Sweep Stage</button>
              <button class="button mr-2 mt-2 is-dark">
                Hide From Stage List
              </button>
              <button class="button mr-2 mt-2 is-danger">Delete Stage</button>
            </template>
            <template v-else>
              <button
                class="button mr-2 mt-2 is-primary"
                :class="{ 'is-loading': loading }"
                @click="createStage"
              >
                Create Stage
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useMutation, useQuery } from "@/services/graphql/composable";
import { stageGraph, userGraph } from "@/services/graphql";
import { inject, reactive, watchEffect } from "vue";
import Field from "@/components/form/Field";
import { notification } from "@/utils/notification";
import { useRouter } from "vue-router";
import { displayName } from "@/utils/auth";

export default {
  components: { Field },
  setup: () => {
    const router = useRouter();
    const stage = inject("stage");
    const id = inject("id");

    const form = reactive({
      ...stage.value,
      id: id.value,
      ownerId: stage.value.owner?.id,
      status: stage.value.attributes.find((a) => a.name === "status")
        .description,
    });
    watchEffect(() => {
      console.log(form);
    });

    const { nodes: users } = useQuery(userGraph.userList);
    const { loading, mutation, data } = useMutation(
      id.value ? stageGraph.updateStage : stageGraph.createStage,
      form
    );
    const createStage = async () => {
      try {
        await mutation();
        notification.success(
          "Stage created successfully! ID: " + data.value.createStage.stage.id
        );
        router.push(
          `/dashboard/stage-management/${data.value.createStage.stage.id}/`
        );
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

    return { id, form, createStage, updateStage, loading, users, displayName };
  },
};
</script>

<style>
</style>