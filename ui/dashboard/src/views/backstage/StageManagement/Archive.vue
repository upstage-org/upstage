<template>
  <teleport to="#main-content .hero-body .title">
    <span style="float: right">
      <button class="button ml-2 is-light" @click="downloadChatLog()">
        <span>Download All Chat</span>
      </button>
      <ClearChat />
      <SweepStage>Archive Performance</SweepStage>
    </span>
  </teleport>

  <DataTable :data="sessions" :headers="headers">
    <template #name="{ item }">
      <div v-if="item.name">
        <b>{{ item.name }}</b>
      </div>
      <small v-if="item.description" class="has-text-dark">
        {{ item.description }}
      </small>
      <small v-else class="has-text-dark">
        <span v-if="item.recording">Recorded </span>
        <span v-else>Auto recorded </span>
        <span v-if="item.chatless">on {{ date(item.createdOn) }}</span>
        <span v-else>
          from {{ date(item.begin) }} to {{ date(item.end) }}
        </span>
      </small>
    </template>
    <template #chat="{ item }">
      <Modal>
        <template #trigger>
          <button class="button is-light">
            <Icon src="chat.svg" />
          </button>
        </template>
        <template #header>
          Chats from {{ date(item.begin) }}
          <span v-if="item.begin !== item.end"> to {{ date(item.end) }}</span>
        </template>
        <template #content>
          <Messages :messages="item.messages" />
        </template>
      </Modal>
      <button class="button is-light" @click="downloadChatLog(item)">
        <Icon src="download.svg" />
      </button>
    </template>
    <template #replay="{ item }">
      <router-link
        :to="`/replay/${stage.fileLocation}/${item.id}`"
        :class="`button ${item.recording ? 'is-primary' : 'is-dark'}`"
      >
        <i class="fas fa-video"></i>
      </router-link>
    </template>
    <template #actions="{ item }">
      <Confirm
        @confirm="(complete) => updatePerformance(item, complete)"
        :loading="updating"
        :only-yes="true"
      >
        <Field v-model="item.name" label="Performance Name" required />
        <Field label="Description">
          <textarea
            class="textarea"
            v-model="item.description"
            rows="3"
          ></textarea>
        </Field>
        <template #yes>
          <span>Save</span>
        </template>
        <template #trigger>
          <button class="button is-light">
            <Icon src="edit.svg" />
          </button>
        </template>
      </Confirm>
      <Confirm
        @confirm="(complete) => deletePerformance(item, complete)"
        :loading="deleting"
      >
        <template #trigger>
          <button class="button is-light is-danger">
            <Icon src="delete.svg" />
          </button>
        </template>
        <div class="has-text-centered">
          Deleting this performance will also delete
          <span class="has-text-danger">all of its replay and chat</span>. This
          cannot be undo!
          <strong>Are you sure you want to continue?</strong>
        </div>
      </Confirm>
    </template>
  </DataTable>
</template>

<script>
import Messages from "@/components/stage/Chat/Messages";
import DataTable from "@/components/DataTable";
import Modal from "@/components/Modal";
import Icon from "@/components/Icon";
import Confirm from "@/components/Confirm";
import Field from "@/components/form/Field";
import ClearChat from "./ClearChat";
import SweepStage from "./SweepStage";
import { computed, inject } from "@vue/runtime-core";
import moment from "moment";
import humanizeDuration from "humanize-duration";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";

export default {
  components: {
    Messages,
    DataTable,
    ClearChat,
    SweepStage,
    Modal,
    Icon,
    Confirm,
    Field,
  },
  setup: () => {
    const stage = inject("stage");
    const refresh = inject("refresh");

    const date = (value) => {
      return value ? moment(value).format("YYYY-MM-DD") : "Now";
    };

    const headers = [
      {
        title: "Name",
        slot: "name",
      },
      {
        title: "Chat",
        slot: "chat",
        align: "center",
      },
      {
        title: "Replay",
        slot: "replay",
      },
      {
        title: "Messages",
        render: (item) => item.messages.length,
        align: "center",
      },
      {
        title: "Length",
        render: (item) => humanizeDuration(item.duration, { round: true }),
        align: "center",
      },
      {
        title: "Archived On",
        key: "createdOn",
        type: "date",
      },
      {
        title: "",
        slot: "actions",
      },
    ];

    const sessions = computed(() => {
      const res = [];
      if (stage.value) {
        const { performances, chats } = stage.value;
        performances.forEach((p) => {
          p.messages = chats
            .filter((c) => c.performanceId === p.id)
            .map((c) => JSON.parse(c.payload));
          res.push(p);
        });
      }
      res.sort((a, b) => b.id - a.id);
      res.forEach((session) => {
        const messages = session.messages.filter((m) => !m.clear);
        if (messages.length) {
          session.begin = messages[0].at;
          session.end = messages[messages.length - 1].at;
          session.duration = session.end - session.begin;
        } else {
          session.chatless = true;
          session.duration = 0;
        }
      });
      return res;
    });

    let textFile;

    const makeTextFile = function (content) {
      const data = new Blob(content, { type: "text/plain" });

      // If we are replacing a previously generated file we need to
      // manually revoke the object URL to avoid memory leaks.
      if (textFile !== null) {
        window.URL.revokeObjectURL(textFile);
      }

      textFile = window.URL.createObjectURL(data);

      // returns a URL you can use as a href
      return textFile;
    };

    const downloadChatLog = (session) => {
      const link = document.createElement("a");
      let content = [];

      if (session) {
        link.setAttribute(
          "download",
          `[Chat] ${stage.value.name} (${
            session.end ? date(session.end) : "Now"
          }).txt`
        );
        content = session.messages.map((item) => {
          let line = "";
          if (item.clear) {
            line = "---------------- Clear Chat ----------------";
          } else {
            line = `${item.user}: ${item.message}`;
          }
          return `${line}\r\n`;
        });
      } else {
        link.setAttribute("download", `[Chat] ${stage.value.name}.txt`);
        sessions.value.forEach((session) => {
          content = content.concat(
            session.messages.map((item) => `${item.user}: ${item.message}\r\n`)
          );
        });
        link.href = makeTextFile(content);
      }
      link.href = makeTextFile(content);
      document.body.appendChild(link);

      // wait for the link to be added to the document
      window.requestAnimationFrame(function () {
        const event = new MouseEvent("click");
        link.dispatchEvent(event);
        document.body.removeChild(link);
      });
    };

    const { loading: updating, save: updateMutation } = useMutation(
      stageGraph.updatePerformance
    );
    const updatePerformance = async (item, complete) => {
      await updateMutation(
        "Performance updated successfully!",
        item.id,
        item.name,
        item.description
      );
      complete();
    };

    const { loading: deleting, save: deleteMutation } = useMutation(
      stageGraph.deletePerformance
    );
    const deletePerformance = async (item, complete) => {
      await deleteMutation("Performance deleted successfully!", item.id);
      complete();
      if (refresh) {
        refresh(stage.value.id);
      }
    };

    return {
      stage,
      sessions,
      downloadChatLog,
      headers,
      date,
      updatePerformance,
      updating,
      deletePerformance,
      deleting,
    };
  },
};
</script>

<style>
</style>