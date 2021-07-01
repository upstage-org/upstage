<template>
  <Tabs v-if="tabs.length" :items="tabs">
    <template v-for="tab in tabs" :key="tab.key" v-slot:[tab.key]>
      <Messages :messages="tab.messages" />
      <teleport to="#main-content .hero-body .title">
        <span style="float: right">
          <button class="button ml-2 is-light" @click="downloadChatLog(tab)">
            <span>Save Chat</span>
          </button>
          <button class="button ml-2 is-light" @click="downloadChatLog()">
            <span>Save All Chat</span>
          </button>
          <ClearChat />
        </span>
      </teleport>
    </template>
  </Tabs>
  <Messages v-else :messages="[]" />
</template>

<script>
import Messages from "@/components/stage/Chat/Messages";
import Tabs from "@/components/Tabs.vue";
import ClearChat from "./ClearChat";
import { computed, inject } from "@vue/runtime-core";
import moment from "moment";

export default {
  components: { Messages, Tabs, ClearChat },
  setup: () => {
    const stage = inject("stage");

    const time = (value) => {
      return moment(value).format("YYYY-MM-DD");
    };

    const tabs = computed(() => {
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
      res = res.filter((tab, i) => i === res.length - 1 || tab.messages.length);
      res.reverse();
      res.forEach((tab) => {
        if (tab.messages.length === 0) {
          tab.label = "now";
        } else {
          const begin = time(tab.messages[0].at);
          const end = time(tab.messages[tab.messages.length - 1].at);
          if (begin === end) {
            tab.label = `${begin}`;
          } else {
            tab.label = `${end} ➜ ${begin}`;
          }
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

    const downloadChatLog = (tab) => {
      const link = document.createElement("a");
      let content = [];

      if (tab) {
        link.setAttribute(
          "download",
          `[Chat] ${stage.value.name} (${tab.label}).txt`
        );
        content = tab.messages.map(
          (item) => `${item.user}: ${item.message}\r\n`
        );
      } else {
        link.setAttribute("download", `[Chat] ${stage.value.name}.txt`);
        tabs.value.forEach((tab) => {
          content = content.concat(
            tab.messages.map((item) => `${item.user}: ${item.message}\r\n`)
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
    return { tabs, downloadChatLog };
  },
};
</script>

<style>
</style>