<template>
  <teleport to="#main-content .hero-body .title">
    <span style="float: right">
      <button class="button ml-2 is-light" @click="downloadChatLog()">
        <span>Save All Chat</span>
      </button>
      <ClearChat />
    </span>
  </teleport>

  <DataTable :data="sessions" :headers="headers">
    <template #view="{ item }">
      <Modal>
        <template #trigger>
          <button class="button is-light is-small">
            <i class="fas fa-lg fa-eye has-text-primary" />
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
    </template>
    <template #download="{ item }">
      <button class="button is-light is-small" @click="downloadChatLog(item)">
        <i class="fas fa-lg fa-download has-text-primary" />
      </button>
    </template>
  </DataTable>
</template>

<script>
import Messages from "@/components/stage/Chat/Messages";
import DataTable from "@/components/DataTable";
import Modal from "@/components/Modal";
import ClearChat from "./ClearChat";
import { computed, inject } from "@vue/runtime-core";
import moment from "moment";

export default {
  components: { Messages, DataTable, ClearChat, Modal },
  setup: () => {
    const stage = inject("stage");

    const date = (value) => {
      return moment(value).format("YYYY-MM-DD");
    };

    const ago = (value) => {
      return moment(value).fromNow();
    };

    const headers = [
      {
        title: "From",
        key: "begin",
        render: ({ begin }) => (begin ? date(begin) : "Now"),
      },
      {
        title: "To",
        key: "end",
        render: ({ end }) => (end ? date(end) : "Now"),
      },
      {
        title: "Cleared On",
        description:
          "The first row is blank because these chat was not cleared",
        key: "clearedOn",
        render: ({ end }) => (end ? ago(end) : ""),
      },
      {
        title: "View",
        slot: "view",
        align: "center",
      },
      {
        title: "Download",
        slot: "download",
        align: "center",
      },
    ];

    const sessions = computed(() => {
      let res = [
        {
          key: 0,
          messages: [],
        },
      ];
      if (stage.value) {
        stage.value.chats.forEach((chat) => {
          if (chat.payload) {
            const event = JSON.parse(chat.payload);
            if (event.clear) {
              res.push({
                key: res.length,
                messages: [],
              });
            } else {
              res[res.length - 1].messages.push(event);
            }
          }
        });
      }
      res = res.filter(
        (session, i) => i === res.length - 1 || session.messages.length
      );
      res.reverse();
      res.forEach((session) => {
        if (session.messages.length) {
          session.begin = session.messages[0].at;
          session.end = session.messages[session.messages.length - 1].at;
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
        content = session.messages.map(
          (item) => `${item.user}: ${item.message}\r\n`
        );
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
    return { sessions, downloadChatLog, headers, date };
  },
};
</script>

<style>
</style>