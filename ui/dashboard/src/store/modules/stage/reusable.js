import configs from "@/config";
import store from "@/store";

export function toRelative(size) {
  const stageSize = store.getters["stage/stageSize"];
  return size / stageSize.width;
}

export function toAbsolute(size) {
  const stageSize = store.getters["stage/stageSize"];
  return size * stageSize.width;
}

export function recalcFontSize(object, f) {
  if (object.type === "text") {
    object.fontSize = f(object.fontSize.slice(0, -2)) + "px";
  }
}

export function serializeObject(object) {
  const { src, type } = object;
  object = {
    ...object,
    src: type === "stream" ? null : src,
  };
  object.x = toRelative(object.x);
  object.y = toRelative(object.y);
  object.w = toRelative(object.w);
  object.h = toRelative(object.h);
  recalcFontSize(toRelative);
  return object;
}

export function deserializeObject(object) {
  if (object.type === "stream") {
    delete object.src;
  }
  object.x = toAbsolute(object.x);
  object.y = toAbsolute(object.y);
  object.w = toAbsolute(object.w);
  object.h = toAbsolute(object.h);
  recalcFontSize(toAbsolute);
  return object;
}

export function namespaceTopic(topicName, stageUrl) {
  const url = stageUrl ?? store.getters["stage/url"];
  const namespace = configs.MQTT_NAMESPACE;
  return `${namespace}/${url}/${topicName}`;
}

export function unnamespaceTopic(topicName) {
  const url = store.getters["stage/url"];
  const namespace = configs.MQTT_NAMESPACE;
  return topicName.substring(namespace.length + url.length + 2);
}

export function getDefaultStageConfig() {
  return {
    animateDuration: 1000,
    reactionDuration: 5000,
    ratio: 16 / 9,
  };
}

export function getDefaultStageSettings() {
  return {
    chatVisibility: true,
    chatDarkMode: false,
    reactionVisibility: true,
  };
}

export function takeSnapshotFromStage() {
  const {
    background,
    backdropColor,
    board: originalBoard,
    settings,
    audioPlayers,
    tools,
  } = store.state.stage;
  const board = Object.assign({}, originalBoard);
  board.objects = originalBoard.objects
    .filter((o) => o.liveAction)
    .map(serializeObject);
  board.tracks = [];
  const payload = JSON.stringify({
    background,
    backdropColor,
    board,
    settings,
    audioPlayers,
    audios: tools.audios,
  });
  tools.audios?.forEach((audio) => {
    store.dispatch("stage/updateAudioStatus", {
      ...audio,
      isPlaying: false,
    });
  });
  return payload;
}
