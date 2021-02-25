<template>
  <div>
    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Full Name</label>
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
      disabled
      horizontal
      label="Email"
      placeholder="Email"
      v-model="form.email"
    />
    <Field horizontal label="Phone" placeholder="Phone" v-model="form.phone" />
    <Field
      horizontal
      label="Apartment"
      placeholder="Apartment"
      v-model="form.apartment"
    />
    <div class="field is-horizontal">
      <div class="field-label"><label class="label">Status</label></div>
      <div class="field-body">
        <div class="field is-narrow">
          <div class="control">
            <Switch
              :modelValue="true"
              className="is-rounded is-success"
              label="Active"
              disabled
            />
            &nbsp;
            <Switch
              v-model="form.agreedToTerms"
              className="is-rounded is-success"
              label="Agreed to terms"
            />
            &nbsp;
            <Switch
              v-model="form.okToSms"
              className="is-rounded is-success"
              label="OK to SMS"
            />
            &nbsp;
            <Switch
              v-model="form.acceptRentPayment"
              className="is-rounded is-success"
              label="Accept rent payment"
            />
          </div>
        </div>
      </div>
    </div>

    <ActionsField>
      <button
        class="button mr-2 mt-2 is-primary"
        :class="{ 'is-loading': loading }"
        @click="updateInformation"
      >
        Update Information
      </button>
    </ActionsField>
  </div>
</template>

<script>
import Field from "@/components/form/Field";
import ActionsField from "@/components/form/ActionsField";
import Switch from "@/components/form/Switch";
import { useStore } from "vuex";
import { reactive } from "vue";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
export default {
  components: { Field, Switch, ActionsField },
  setup: () => {
    const store = useStore();
    const form = reactive(store.state.user.user);
    const { loading, mutation: updateUser } = useMutation(
      userGraph.updateUser,
      form
    );
    const updateInformation = async () => {
      try {
        await updateUser();
        notification.success("Player information updated successfully!");
      } catch (error) {
        notification.error(error);
      }
    };

    return { form, updateInformation, loading };
  },
};
</script>

<style>
</style>