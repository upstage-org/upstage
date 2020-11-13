<template>
  <v-container fluid class=" mb-6 dashboard-container">
    <v-row no-gutters class="stage-row">
      <v-col class="stage-menu" cols="2">
        <v-img src="@/assets/upstage.png"></v-img>
        <v-list>
          <v-list-item>statistics</v-list-item>
          <v-list-item>statement</v-list-item>
          <v-list-item>live</v-list-item>
          <v-list-item>avatar</v-list-item>
          <v-list-item>scene</v-list-item>
          <v-select :items="items" label="Solo field" dense solo></v-select>
        </v-list>
      </v-col>
      <v-col class="stage-board" cols="7"> </v-col>
      <v-col class="stage-chat" cols="3">
        <div class="stage-chat-board">
          <v-list>
            <v-list-item v-for="chat in chats" :key="chat.title">
              <v-list-item-avatar>
                <v-img src="@/assets/defaultava.png"></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-html="chat.title"></v-list-item-title>
                <v-list-item-subtitle
                  v-html="chat.subtitle"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <v-text-field
          v-model="message"
          label="Enter Message"
          append-outer-icon="mdi-emoticon-outline"
        ></v-text-field>
        <v-btn tile color="success" @click="addShape">
          <v-icon left>
            mdi-send
          </v-icon>
          Send
        </v-btn>
        <v-btn @click="createConnection">Connect</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { shapeCommand } from "@/utils/constants";
import mqtt from "mqtt";
export default {
  data: () => ({
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    message: "",
    items: ["Stage Test"],
    chats: [],
    connection: {
      host: "broker.emqx.io",
      port: 8083,
      endpoint: "/mqtt",
      clean: true, // Reserved session
      connectTimeout: 4000, // Time out
      reconnectPeriod: 4000, // Reconnection interval
      // Certification Information
      clientId: "mqttjs_3be2c321",
      username: "emqx_test",
      password: "emqx_test",
    },
    subscription: {
      topic: "topic/mqttx",
      qos: 0,
    },
    publish: {
      topic: "topic/command",
      qos: 2,
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
  },
  methods: {
    addShape() {
      if (shapeCommand[this.message]) {
        const target = document.getElementsByClassName("stage-board");
        const temp = document.createElement("span");
        const classname = shapeCommand[this.message];
        temp.className = classname;
        target[0].appendChild(temp);
      } else {
        const newMessage = {
          title: "unititled",
          subtitle: this.message,
        };
        this.chats.push(newMessage);
      }
      this.message = "";
    },
    // Create connection
    createConnection() {
      // Connect string, and specify the connection method used through protocol
      // ws unencrypted WebSocket connection
      // wss encrypted WebSocket connection
      // mqtt unencrypted TCP connection
      // mqtts encrypted TCP connection
      // wxs WeChat mini app connection
      // alis Alipay mini app connection
      const { host, port, endpoint, ...options } = this.connection;
      const connectUrl = `mqtt://${host}:${port}${endpoint}`;

      try {
        this.client = mqtt.connect(connectUrl, options);
        console.log(connectUrl);
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
        this.receiveNews = this.receiveNews.concat(message);
        console.log(`Received message ${message} from topic ${topic}`);
      });
    },
    doSubscribe() {
      const { topic, qos } = this.subscription;
      this.client.subscribe(topic, { qos }, (error, res) => {
        if (error) {
          console.log("Subscribe to topics error", error);
          return;
        }
        this.subscribeSuccess = true;
        console.log("Subscribe to topics res", res);
      });
    },
  },
};
</script>

<style scope>
.dashboard-container {
  height: 100%;
  padding: 0;
  border: 5px solid #006600 !important;
}
.stage-row {
  height: 100%;
}
.stage-board {
  background-color: black;
}
.stage-chat {
  padding: 8px !important;
}
.stage-chat-board {
  border: 5px solid green !important;
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
</style>
