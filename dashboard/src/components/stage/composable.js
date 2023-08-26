import { onUnmounted, ref } from "vue";
import buildClient from "@/services/mqtt";
import { BACKGROUND_ACTIONS, TOPICS } from "@/utils/constants";
import { namespaceTopic } from "@/store/modules/stage/reusable";

export const useCounter = (stageUrl) => {
  const players = ref(0);
  const audiences = ref(0);
  const loading = ref(true);

  const mqtt = buildClient();
  const client = mqtt.connect();
  client.on("connect", () => {
    const topics = {
      [TOPICS.STATISTICS]: { qos: 2 },
    };
    mqtt.subscribe(topics, stageUrl).then(() => {
      loading.value = false;
    });
  });
  client.on("error", (e) => {
    console.log(e);
  });
  mqtt.receiveMessage(({ message }) => {
    players.value = message.players;
    audiences.value = message.audiences;
  });

  onUnmounted(() => {
    mqtt.disconnect();
  });

  return [players, audiences, loading];
};

export const useShortcut = (callback) => {
  const shortcutHandler = (e) => {
    if (!e) e = window.event;
    callback(e);
  };

  window.addEventListener("keydown", shortcutHandler);

  onUnmounted(() => {
    window.removeEventListener("keydown", shortcutHandler);
  });
};

export const useHoldingShift = () => {
  const isHoldingShift = ref(false);

  const callback = (e) => {
    if (!e) e = window.event;
    if (e.shiftKey) {
      isHoldingShift.value = true;
    } else {
      isHoldingShift.value = false;
    }
  };
  window.addEventListener("keydown", callback);
  window.addEventListener("keyup", callback);

  onUnmounted(() => {
    window.removeEventListener("keydown", callback);
    window.removeEventListener("keyup", callback);
  });

  return isHoldingShift;
};

export const useClearStage = (stageUrl) => {
  const mqttClient = buildClient();
  const clearStage = async () => {
    await new Promise((resolve) => {
      mqttClient.connect().on("connect", () => {
        mqttClient
          .sendMessage(
            namespaceTopic(TOPICS.BACKGROUND, stageUrl),
            { type: BACKGROUND_ACTIONS.BLANK_SCENE },
            true,
          )
          .then(resolve);
      });
    });
  };

  return clearStage;
};
