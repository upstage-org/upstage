<template>
  <div id="chatbox" class="card is-light">
    <div class="card-content" ref="theContent">
      <div v-if="!messages.length" class="columns is-vcentered is-fullheight">
        <div class="column has-text-centered has-text-light">
          <i class="fas fa-comments fa-4x"></i>
          <p class="title has-text-light">No messages yet!</p>
        </div>
      </div>
      <div v-else>
        <p v-for="item in messages" :key="item">
          <small>
            <strong>{{ item.name }}</strong> <time>{{ item.at }}</time>
          </small>
          <br />
          {{ item.content }}
        </p>
      </div>
    </div>
    <footer class="card-footer">
      <div class="card-footer-item">
        <div class="control has-icons-right is-fullwidth">
          <input
            class="input is-rounded"
            placeholder="Type message"
            v-model="message"
            @keydown.enter="sendMessage"
          />
          <span
            class="icon is-right clickable button is-primary is-rounded"
            @click="sendMessage"
          >
            <i class="fas fa-paper-plane"></i>
          </span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import moment from "moment";
import anime from "animejs";

export default {
  setup: () => {
    const theContent = ref();

    const messages = reactive([]);
    const message = ref("");
    const scrollToEnd = () => {
      anime({
        targets: theContent.value,
        scrollTop: theContent.value?.scrollHeight,
        easing: "easeInOutQuad",
      });
    };
    const sendMessage = () => {
      if (message.value.trim()) {
        messages.push({
          name: "Me",
          at: moment().format("hh:mm"),
          content: message.value,
        });
        message.value = "";
        scrollToEnd();
      }
    };

    return {
      messages,
      message,
      sendMessage,
      theContent,
    };
  },
};
</script>

<style lang="scss" scoped>
#chatbox {
  position: fixed;
  width: 20%;
  min-width: 200px;
  height: calc(100vh - 75px);
  bottom: 16px;
  right: 16px;
  opacity: 0.9;

  .card-content {
    height: calc(100vh - 140px);
    overflow-y: auto;
  }

  time {
    float: right;
  }
}
</style>