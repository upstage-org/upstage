import config from '@/config'
import { v4 as uuidv4 } from "uuid";
import mqtt from "mqtt";

const mqttService = {
  client: null,
  connect() {
    const { host, port, endpoint, ...options } = config.MQTT_CONNECTION;
    const connectUrl = `ws://${host}:${port}${endpoint}`;
    const clientId = uuidv4();
    this.client = mqtt.connect(connectUrl, {
      ...options,
      clientId,
    });
    return this.client;
  },
  disconnect() {
    return new Promise((resolve) => {
      this.client.end(false, {}, resolve)
    });
  },
  subscribe(topics) {
    return new Promise((resolve, reject) => {
      this.client.subscribe(
        topics,
        (error, res) => {
          if (error) {
            reject(error)
          } else {
            resolve(res)
          }
        }
      );
    })
  },
  sendMessage(topic, payload) {
    let message = payload;
    if (typeof payload === "object") {
      message = JSON.stringify(payload);
    }
    return new Promise((resolve, reject) => {
      this.client.publish(
        topic,
        message,
        {
          qos: 1,
          retain: true,
          properties: {
            userProperties: "upstage",
          },
        },
        (error, res) => {
          if (error) {
            reject(error)
          } else {
            resolve(res)
          }
        }
      );
    })
  }
}

export default mqttService;