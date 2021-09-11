<template>
  <SaveButton :disabled="disabled" :loading="saving" @click="saveBatch" />
  <section>
    <div :key="i" class="field is-grouped">
      <p class="control is-expanded">
        <label class="label">Username</label>
      </p>
      <p class="control is-expanded">
        <label class="label">Password</label>
      </p>
      <p class="control">
        <a
          style="visibility: hidden; height: 0"
          class="button is-danger is-light"
          @click="remove(i)"
        >
          <Icon src="delete.svg" />
        </a>
      </p>
    </div>
    <div v-for="(user, i) in form.users" :key="i" class="field is-grouped">
      <p class="control is-expanded">
        <Field
          v-model="user.username"
          required
          required-message="Username is required for guest to login"
          type="text"
          placeholder="Username"
        />
      </p>
      <p class="control is-expanded">
        <Field
          v-model="user.password"
          required
          required-message="Password is required for guest to login"
          type="text"
          placeholder="Password"
        />
      </p>
      <p class="control">
        <a class="button is-danger is-light" @click="remove(i)">
          <Icon src="delete.svg" />
        </a>
      </p>
    </div>
    <a class="button is-primary is-block" @click="append()">
      <span>New</span>
      <span class="icon">
        <i class="fas fa-plus"></i>
      </span>
    </a>
  </section>
  <section class="my-4">
    <Switch v-model="autoAssign" label="Assign to stages after created" />
    <MultiSelectList
      v-if="autoAssign"
      :loading="loadingStages"
      :data="availableStages"
      v-model="form.assignedStages"
      :columnClass="() => 'is-12 p-0'"
    >
      <template #render="{ item }">
        <div class="box m-0 p-2">
          <div class="content">
            <strong>{{ item.name }}</strong>
            <span style="float: right">
              Created by
              <span class="has-text-primary">
                {{ displayName(item.owner) }}
              </span>
            </span>
          </div>
        </div>
      </template>
    </MultiSelectList>
  </section>
</template>

<script>
import { stageGraph, userGraph } from "@/services/graphql";
import { useMutation, useQuery } from "@/services/graphql/composable";
import Icon from "@/components/Icon";
import Field from "@/components/form/Field";
import Switch from "@/components/form/Switch";
import SaveButton from "@/components/form/SaveButton";
import MultiSelectList from "@/components/MultiSelectList";
import { reactive, ref } from "@vue/reactivity";
import { computed } from "@vue/runtime-core";
import { displayName } from "@/utils/auth";
import { useRouter } from "vue-router";
import { notification } from "@/utils/notification";
import { useStore } from "vuex";

export default {
  components: { Icon, Field, MultiSelectList, Switch, SaveButton },
  setup: () => {
    const store = useStore();
    const router = useRouter();
    const form = reactive({
      users: [],
      assignedStages: [],
    });
    const autoAssign = ref(false);

    const append = () => {
      form.users.push({
        username: "guest" + (form.users.length + 1),
        password: "password",
      });
    };
    append();

    const remove = (i) => {
      form.users.splice(i, 1);
    };

    const { nodes: stageList, loading: loadingStages } = useQuery(
      stageGraph.stageList
    );
    const availableStages = computed(() => {
      if (!stageList.value) return [];
      stageList.value.sort((a, b) => (a.name > b.name ? 1 : -1));
      return stageList.value;
    });

    const { loading: saving, save } = useMutation(userGraph.batchUserCreation);
    const saveBatch = () => {
      save(
        () => {
          store.commit("cache/CLEAR_ALL_GRAPHQL_CACHES");
          notification.success(
            `${form.users.length} users created successfully!`
          );
          router.push("/backstage/admin/player-management");
        },
        {
          users: form.users,
          stageIds: form.assignedStages.map((s) => s.dbId),
        }
      );
    };
    const disabled = computed(() => {
      if (form.users.length === 0) {
        return true;
      }
      for (const user of form.users) {
        if (!user.username || !user.password) {
          return true;
        }
      }
    });

    return {
      form,
      append,
      remove,
      availableStages,
      loadingStages,
      displayName,
      autoAssign,
      saving,
      saveBatch,
      disabled,
    };
  },
};
</script>

<style>
</style>