<template>
  <header class="card-header">
    <p class="card-header-title">Change your nickname</p>
  </header>
  <div class="card-content">
    <div class="content">
      <horizontal-field title="Nickname">
        <input
          class="input"
          type="text"
          :placeholder="nickname"
          v-model="form.nickname"
          @keyup.enter="saveNickname"
        />
      </horizontal-field>
      <save-button @click="saveNickname" :loading="loading" />
    </div>
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import { useStore } from "vuex";
import HorizontalField from "@/components/form/HorizontalField.vue";
import SaveButton from "@/components/form/SaveButton.vue";
import { notification } from "@/utils/notification";
export default {
  components: { HorizontalField, SaveButton },
  setup: (props, { emit }) => {
    const form = reactive({});
    const loading = ref(false);
    const store = useStore();
    const nickname = computed(() => store.getters["user/nickname"]);
    const saveNickname = () => {
      loading.value = true;
      store.dispatch("user/saveNickname", form).then((nickname) => {
        emit("close");
        loading.value = false;
        notification.success("You new nickname is: " + nickname);
      });
    };
    return { nickname, saveNickname, form, loading };
  },
};
</script>

<style>
</style>