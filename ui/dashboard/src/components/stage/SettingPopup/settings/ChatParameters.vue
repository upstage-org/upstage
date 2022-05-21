<template>
  <header class="card-header">
    <div class="tabs card-header-title p-0">
      <ul>
        <li
          :class="{ 'is-active': currentTab === 'nickname' }"
          @click="currentTab = 'nickname'"
        >
          <a>{{ $t("change_your_nickname") }}</a>
        </li>
        <li
          :class="{ 'is-active': currentTab === 'params' }"
          @click="currentTab = 'params'"
        >
          <a>{{ $t("parameters") }}</a>
        </li>
      </ul>
    </div>
  </header>
  <div class="card-content">
    <div class="content" v-if="currentTab === 'nickname'">
      <HorizontalField title="Nickname">
        <input
          class="input"
          type="text"
          :placeholder="nickname"
          v-model="form.nickname"
          @keyup.enter="saveNickname"
        />
      </HorizontalField>
      <SaveButton @click="saveNickname" :loading="loading" />
    </div>
    <div class="content" v-else>
      <HorizontalField title="Chat transparency">
        <input
          v-model="parameters.opacity"
          type="range"
          class="slider is-fullwidth is-primary"
          step="0.01"
          min="0.2"
          max="1"
        />
      </HorizontalField>
      <HorizontalField title="Size (px)">
        <Field
          :modelValue="parameters.fontSize?.slice(0, -2)"
          @update:modelValue="changeFontSize"
          type="number"
        />
      </HorizontalField>

      <save-button @click="saveParameters" />
    </div>
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import { useStore } from "vuex";
import HorizontalField from "@/components/form/HorizontalField.vue";
import Field from "@/components/form/Field";
import SaveButton from "@/components/form/SaveButton.vue";
import { notification } from "@/utils/notification";
export default {
  components: { HorizontalField, Field, SaveButton },
  setup: (props, { emit }) => {
    const form = reactive({});
    const loading = ref(false);
    const store = useStore();
    const nickname = computed(() => store.getters["user/chatname"]);
    const saveNickname = () => {
      loading.value = true;
      store.dispatch("user/saveNickname", form).then((nickname) => {
        emit("close");
        loading.value = false;
        notification.success("You new nickname is: " + nickname);
        loading.value = false;
      });
    };

    const changeFontSize = (value) => {
      parameters.fontSize = value.replace(/^\D+/g, "") + "px";
    };

    const currentTab = ref("nickname");
    const parameters = reactive({
      opacity: store.state.stage.chat.opacity,
      fontSize: store.state.stage.chat.fontSize,
    });
    const saveParameters = () => {
      store.commit("stage/SET_CHAT_PARAMETERS", parameters);
      emit("close");
      notification.success("Chat parameters saved successfully!");
    };

    return {
      nickname,
      saveNickname,
      loading,
      form,
      currentTab,
      parameters,
      saveParameters,
      changeFontSize,
    };
  },
};
</script>

<style>
</style>