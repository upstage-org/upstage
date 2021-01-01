import config from '@/config'
import { v4 as uuidv4 } from "uuid";
import mqtt from "mqtt";
import { topics as defaultTopics } from '@/utils/constants'

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
  subscribe(topic = defaultTopics) {
    return new Promise((resolve, reject) => {
      this.client.subscribe(
        topic,
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
  publish(message, topic) {
    return new Promise((resolve, reject) => {
      if (!topic) {
        const topicNames = Object.keys(defaultTopics);
        topic = topicNames[0]
      }
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