<template>
  <v-container fluid class=" mb-6 dashboard-container">
    <v-row no-gutters class="stage-row">
      <v-col class="stage-menu" cols="2">
        <h2>Tools</h2>
        <v-list class="stage-menu-list">
          <v-list-item>statistics</v-list-item>
          <v-list-item>statement</v-list-item>
          <v-list-item>live</v-list-item>
          <v-list-item>avatar</v-list-item>
          <v-list-item>scene</v-list-item>
          <v-select
            v-show="client.connected"
            :items="items"
            label="Solo field"
            dense
            solo
            v-on:input="doSubscribe"
          ></v-select>
        </v-list>
      </v-col>
      <v-col class="stage-board" cols="7"> </v-col>
      <v-col class="stage-chat" cols="3">
        <div class="stage-chat-board">
          <v-row no-gutters>
            <v-col cols="6">Live</v-col>
            <v-col cols="6"><v-img src="@/assets/upstage.png"></v-img></v-col>
          </v-row>
          <v-list>
            <v-list-item v-for="chat in chats" :key="chat.title">
              <v-list-item-avatar>
                <v-img src="@/assets/defaultava.png"></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title
                  :style="{ color: chatColor }"
                  v-html="chat.user"
                ></v-list-item-title>
                <v-list-item-subtitle
                  v-html="chat.message"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <v-text-field
          v-model="message"
          label="Enter Message"
          append-icon="mdi-emoticon-outline"
          @keyup.enter="doPublish"
          @click:append="show"
        ></v-text-field>
        <v-menu
          v-model="showMenu"
          :position-x="x"
          :position-y="y"
          absolute
          offset-y
        >
          <v-card>
            <v-row>
              <v-col
                v-for="shape in listShapes"
                :key="shape"
                @click="doPublishShape(shape)"
                ><v-icon>mdi-{{ shape }}</v-icon></v-col
              >
            </v-row>
          </v-card>
        </v-menu>
        <v-btn tile color="success" @click="doPublish">
          <v-icon left>
            mdi-send
          </v-icon>
          Send
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { shapeCommand } from "@/utils/constants";
import { isJson, getRandomColor } from "@/utils/common";
import { v4 as uuidv4 } from "uuid";
import mqtt from "mqtt";
export default {
  data: () => ({
    showMenu: false,
    x: 0,
    y: 0,
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    message: "",
    items: ["Stage Test"],
    chats: [],
    chatColor: "",
    shape: [],
    listShapes: ["square", "circle", "triangle"],
    connection: {
      host: "128.199.69.170",
      port: 9001,
      endpoint: "/mqtt",
      clean: true, // Reserved session
      connectTimeout: 4000, // Time out
      reconnectPeriod: 4000, // Reconnection interval
      // Certification Information
      retain: true,
    },
    subscription: {
      topic: "topic/commands",
      qos: 1,
    },
    publish: {
      topic: "topic/commands",
      qos: 1,
      payload: '{ "msg": "Hello, I am browser." }',
    },
    receiveNews: "",
    qosList: [
      { label: 0, value: 0 },
      { label: 1, value: 1 },
      { label: 2, value: 2 },
    ],
    client: {
      connected: false,
    },
    subscribeSuccess: false,
  }),
  created() {
    this.$store.dispatch("user/fetchCurrent");
    this.createConnection();
    this.chatColor = getRandomColor();
  },
  methods: {
    show(e) {
      e.preventDefault();
      this.showMenu = false;
      this.x = e.clientX;
      this.y = e.clientY - 100;
      this.$nextTick(() => {
        this.showMenu = true;
      });
    },
    addShape(e) {
      if (shapeCommand[e]) {
        const target = document.getElementsByClassName("stage-board");
        const temp = document.createElement("span");
        const classname = shapeCommand[e];
        temp.className = classname;
        target[0].appendChild(temp);
      }
    },
    // Create connection
    createConnection() {
      // 连接字符串, 通过协议指定使用的连接方式
      // ws 未加密 WebSocket 连接
      // wss 加密 WebSocket 连接
      // mqtt 未加密 TCP 连接
      // mqtts 加密 TCP 连接
      // wxs 微信小程序连接
      // alis 支付宝小程序连接
      const { host, port, endpoint, ...options } = this.connection;
      const connectUrl = `ws://${host}:${port}${endpoint}`;
      try {
        const clientId = uuidv4();
        console.log(clientId);
        this.client = mqtt.connect(connectUrl, {
          ...options,
          clientId,
        });
      } catch (error) {
        console.log("mqtt.connect error", error);
      }
      this.client.on("connect", () => {
        console.log("Connection succeeded!");
      });
      this.client.on("error", (error) => {
        console.log("Connection failed", error);
      });
      this.client.on("message", (topic, message) => {
        const arr = new TextDecoder().decode(new Uint8Array(message));

        if (topic === "topic/commands") {
          const convertedMessage = (isJson(arr) && JSON.parse(arr)) || arr;
          const modelMessage = {};
          if (typeof convertedMessage === "object") {
            modelMessage.user = convertedMessage.user;
            modelMessage.message = convertedMessage.message;
          } else {
            modelMessage.user = "Anonymous";
            modelMessage.message = convertedMessage;
          }
          this.chats.push(modelMessage);
        } else if (topic === "topic/board") {
          this.addShape(arr);
        }
      });
    },
    // 订阅主题
    doSubscribe() {
      const { topic, qos } = this.subscription;
      this.client.subscribe(
        { [topic]: { qos: 2 }, "topic/board": { qos: 2 } },
        { qos },
        (error, res) => {
          if (error) {
            console.log("Subscribe to topics error", error);
            return;
          }
          this.subscribeSuccess = true;
          console.log("Subscribe to topics res", res);
        }
      );
    },
    doPublishShape(e) {
      const topic = "topic/board";
      const shapeMessage = e;
      this.client.publish(topic, shapeMessage, { qos: 2 });
    },
    // 取消订阅
    doUnSubscribe() {
      const { topic } = this.subscription;
      this.client.unsubscribe(topic, (error) => {
        if (error) {
          console.log("Unsubscribe error", error);
        }
      });
    },
    // 发送消息
    doPublish() {
      const { topic, qos } = this.publish;
      const currentUser = this.$store.getters["user/getCurrentUser"];
      if (!this.message) return;
      const messageModel = {
        user: currentUser,
        message: this.message,
      };
      const converted = JSON.stringify(messageModel);
      this.client.publish(
        topic,
        converted,
        {
          qos,
          retain: true,
          properties: {
            userProperties: "Anh Khoa",
          },
        },
        (error) => {
          this.message = "";
          console.log(topic, this.message);
          if (error) {
            console.log("Publish error", error);
          }
        }
      );
    },
    // 断开连接
    destroyConnection() {
      if (this.client.connected) {
        try {
          this.client.end();
          this.client = {
            connected: false,
          };
          console.log("Successfully disconnected!");
        } catch (error) {
          console.log("Disconnect failed", error.toString());
        }
      }
    },
  },

  beforeDestroy() {
    this.destroyConnection();
  },
};
</script>

<style scope>
.dashboard-container {
  height: 100%;
  padding: 0;
}
.stage-menu {
  background-color: #808080;
}
.stage-menu-list {
  background: transparent !important;
}
.v-list {
  margin-bottom: 0;
  padding: 0;
}
.v-list-item {
  background-color: #fafafa;
  margin: 8px 16px;
  border-radius: 3px;
}
.stage-row {
  height: 100%;
}
.stage-board {
  background-color: black;
}
.stage-chat {
  padding: 8px !important;
  background-color: #363636;
}
.stage-chat-board {
  height: 80%;
}
.stage-shape {
  display: inline-block;
  margin: 0 4px;
}
.bgc-red {
  background-color: red;
}
.bgc-blue {
  background-color: blue;
}
.bgc-yellow {
  background-color: yellow;
}
.bgc-white {
  background-color: white;
}
.square {
  width: 40px;
  height: 40px;
}
.circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.triangle {
  width: 0;
  height: 0;
  border-left: 18px solid transparent;
  border-right: 18px solid transparent;
  border-bottom: 40px solid red;
}
.v-icon {
  cursor: pointer;
  padding: 0 4px;
}
</style>
