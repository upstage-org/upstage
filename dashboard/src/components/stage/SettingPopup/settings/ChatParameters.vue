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
        <li
          v-if="downloadChatVisibility"
          :class="{ 'is-active': currentTab === 'download' }"
          @click="currentTab = 'download'"
        >
          <a>{{ $t("download_chat") }}</a>
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
    <div class="content" v-else-if="currentTab === 'params'">
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
    <div class="content" v-else>
      <h4>Select the sections you want to download</h4>
      <div class="field is-horizontal">
        <div class="field-label">
          <label class="label fix">{{ $t("audience_chat") }}</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <Switch
              :data-tooltip="downloadOptions.audienceChat ? 'On' : 'Off'"
              v-model="downloadOptions.audienceChat"
            />
          </div>
        </div>
      </div>
      <div class="field is-horizontal">
        <div class="field-label">
          <label class="label fix">{{ $t("player_chat") }}</label>
        </div>
        <div class="field-body">
          <div class="field is-narrow">
            <Switch
              :data-tooltip="downloadOptions.playerChat ? 'On' : 'Off'"
              v-model="downloadOptions.playerChat"
            />
          </div>
        </div>
      </div>

      <DownloadButton
        @click="downloadChatLog"
        v-if="downloadOptions.audienceChat || downloadOptions.playerChat"
      />
      <DownloadButton disabled v-else />
    </div>
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import { useStore } from "vuex";
import HorizontalField from "@/components/form/HorizontalField.vue";
import Field from "@/components/form/Field";
import SaveButton from "@/components/form/SaveButton.vue";
import DownloadButton from "@/components/form/DownloadButton.vue";
import { notification } from "@/utils/notification";
import Switch from "@/components/form/Switch.vue";

export default {
  components: { HorizontalField, Field, SaveButton, Switch, DownloadButton },
  setup: (props, { emit }) => {
    const form = reactive({});
    const loading = ref(false);
    const store = useStore();
    const nickname = computed(() => store.getters["user/chatname"]);
    const downloadOptions = ref({
      audienceChat: false,
      playerChat: false,
    });

    const chats = computed(() => store.state.stage.chat);
    const downloadChatVisibility = computed(
      () => store.state.stage.showDownloadChatSetting,
    );
    const stageUrl = store.getters["stage/url"];

    const saveNickname = () => {
      loading.value = true;
      store.dispatch("user/saveNickname", form).then((nickname) => {
        emit("close");
        loading.value = false;
        notification.success("You new nickname is: " + nickname);
        loading.value = false;
      });
    };

    const makeTextFile = function (content) {
      let textFile;
      const data = new Blob(content, { type: "text/plain" });
      if (textFile !== null) {
        window.URL.revokeObjectURL(textFile);
      }
      textFile = window.URL.createObjectURL(data);
      return textFile;
    };

    const downloadChatLog = () => {
      if (downloadOptions.value.audienceChat) {
        let link = document.createElement("a");
        let content = [];
        link.setAttribute(
          "download",
          `${stageUrl}-Audience-chat-${timeStamp()}.txt`,
        );
        content = chats.value.messages.map((item) => {
          let line = "";
          if (item.clear) {
            line = "---------------- Clear Chat ----------------";
          } else {
            line = `${item.user}: ${item.message}`;
          }
          return `${line}\r\n`;
        });
        link.href = makeTextFile(content);
        document.body.appendChild(link);
        window.requestAnimationFrame(function () {
          const event = new MouseEvent("click");
          link.dispatchEvent(event);
          document.body.removeChild(link);
        });
      }

      if (downloadOptions.value.playerChat) {
        let link = document.createElement("a");
        let content = [];
        link.setAttribute(
          "download",
          `${stageUrl}-Player-chat-${timeStamp()}.txt`,
        );
        content = chats.value.privateMessages.map((item) => {
          let line = "";
          if (item.clearPlayerChat) {
            line = "---------------- Clear Chat ----------------";
          } else {
            line = `${item.user}: ${item.message}`;
          }
          return `${line}\r\n`;
        });
        link.href = makeTextFile(content);
        document.body.appendChild(link);
        window.requestAnimationFrame(function () {
          const event = new MouseEvent("click");
          link.dispatchEvent(event);
          document.body.removeChild(link);
        });
      }
      emit("close");
      notification.success("Download success");
    };

    const padTo2Digits = (num) => {
      return num.toString().padStart(2, "0");
    };
    const formatDate = (date) => {
      return (
        [padTo2Digits(date.getHours()), padTo2Digits(date.getMinutes())].join(
          "",
        ) +
        "-" +
        [
          padTo2Digits(date.getDate()),
          padTo2Digits(date.getMonth() + 1),
          date.getFullYear(),
        ].join("")
      );
    };
    const timeStamp = () => {
      const date = new Date();
      return formatDate(date);
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
      downloadOptions,
      downloadChatVisibility,
      downloadChatLog,
      saveParameters,
      changeFontSize,
    };
  },
};
</script>

<style>
.fix {
  width: 115px;
}
</style>
