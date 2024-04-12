<template>
  <div style="width: 500px">
    <ChatInput
      v-model="message"
      placeholder="Type message"
      @keyup.enter="sendChat"
    />
  </div>
</template>

<script>
import ChatInput from "components/form/ChatInput.vue";
import { ref } from "vue";
import { useStore } from "vuex";
export default {
  components: { ChatInput },
  emits: ["close"],
  setup: (props, { emit }) => {
    const store = useStore();
    const message = ref("");
    const sendChat = () => {
      if (message.value.trim()) {
        store
          .dispatch("stage/sendChat", { message: message.value })
          .then(() => {
            message.value = "";
            emit("close");
          });
      }
    };

    return { message, sendChat };
  },
};
</script>

<style></style>
