<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Stage Name</label>
      </div>
      <div class="field-body">
        <Field
          placeholder="Full Name"
          v-model="stage.name"
          required
          requiredMessage="Stage name is required"
          expanded
        />
        <Field
          required
          placeholder="Short Name"
          v-model="stage.fileLocation"
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
              v-model="stage.description"
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Media</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <div class="select is-fullwidth">
              <select>
                <option>Media 1</option>
                <option>Media 2</option>
                <option>Media 3</option>
              </select>
            </div>
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
              <select v-model="stage.ownerId">
                <option v-for="user in users" :key="user" :value="user.id">
                  {{ user.displayName ? user.displayName : user.username }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">Stage Status</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <label class="radio">
              <input type="radio" name="status" />
              Live
            </label>
            <label class="radio">
              <input type="radio" name="status" />
              Upcoming
            </label>
            <label class="radio">
              <input type="radio" name="status" />
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
            <button
              class="button mr-2 mt-2 is-primary"
              :class="{ 'is-loading': loading }"
              @click="createStage"
            >
              Save Stage
            </button>
            <button class="button mr-2 mt-2 is-warning">Clear Chat</button>
            <button class="button mr-2 mt-2 is-warning">Sweep Stage</button>
            <button class="button mr-2 mt-2 is-dark">
              Hide From Stage List
            </button>
            <button class="button mr-2 mt-2 is-danger">Delete Stage</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useMutation, useQuery } from "@/services/graphql/composable";
import { stageGraph, userGraph } from "@/services/graphql";
import { reactive, watchEffect } from "vue";
import Field from "@/components/form/Field";
import { notification } from "@/utils/notification";
import { useRouter } from "vue-router";

export default {
  components: { Field },
  setup: () => {
    const stage = reactive({});
    const { loading, mutation, data } = useMutation(
      stageGraph.createStage,
      stage
    );

    const { nodes: users } = useQuery(userGraph.oneUser);
    watchEffect(() => {
      console.log(stage);
    });

    const router = useRouter();
    const createStage = async () => {
      await mutation();
      if (data) {
        notification.success(
          "Stage created successfully! ID: " + data.value.createStage.stage.id
        );
        router.push({
          name: "Stage Management",
          params: {
            id: data.value.createStage.stage.id,
          },
        });
      }
    };

    return { stage, createStage, loading, users, json: JSON.stringify };
  },
};
</script>

<style>
</style>