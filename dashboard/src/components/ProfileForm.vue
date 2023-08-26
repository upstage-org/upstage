<template>
  <form @submit.prevent="updateInformation">
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">{{ $t("full_name") }}</label>
      </div>
      <div class="field-body">
        <Field placeholder="First Name" v-model="form.firstName" />
        <Field placeholder="Last Name" v-model="form.lastName" />
      </div>
    </div>
    <Field
      horizontal
      label="Display Name"
      placeholder="Display Name"
      v-model="form.displayName"
      help="In stage chat nickname"
    />
    <Field
      horizontal
      type="email"
      label="Email"
      placeholder="Email"
      v-model="form.email"
    />
    <div class="field is-horizontal">
      <div class="field-label">
        <label class="label">{{ $t("status") }}</label>
      </div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <Switch
              :modelValue="true"
              className="is-rounded is-success"
              label="Active"
              disabled
            />
          </div>
        </div>
      </div>
    </div>

    <ActionsField>
      <button
        class="button mr-2 mt-2 is-primary"
        :class="{ 'is-loading': loading }"
        type="submit"
      >
        Update Information
      </button>
    </ActionsField>
  </form>
</template>

<script>
import Field from "@/components/form/Field";
import ActionsField from "@/components/form/ActionsField";
import Switch from "@/components/form/Switch";
import { reactive } from "vue";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
export default {
  components: { Field, Switch, ActionsField },
  props: ["profile"],
  emits: ["success"],
  setup: (props, { emit }) => {
    const form = reactive(props.profile);
    const { loading, mutation: updateUser } = useMutation(
      userGraph.updateUser,
      form,
    );
    const updateInformation = async () => {
      try {
        await updateUser();
        notification.success("Player information updated successfully!");
        emit("success");
      } catch (error) {
        notification.error(error);
      }
    };

    return { form, updateInformation, loading };
  },
};
</script>

<style></style>
