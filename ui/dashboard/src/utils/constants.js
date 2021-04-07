export const TOPICS = {
  CHAT: "topic/chat",
  BOARD: "topic/board",
  BACKGROUND: "topic/background",
  AUDIO: "topic/audio",
  REACTION: "topic/reaction",
  COUNTER: "topic/counter",
}

export const BOARD_ACTIONS = {
  PLACE_OBJECT_ON_STAGE: 'placeObjectOnStage',
  MOVE_TO: 'moveTo',
  DESTROY: 'destroy',
  SWITCH_FRAME: 'switchFrame',
  SPEAK: 'speak',
  BRING_TO_FRONT: 'bringToFront',
  SEND_TO_BACK: 'sendToBack',
  TOGGLE_AUTOPLAY_FRAMES: 'toggleAutoplayFrames',
}

export const ROLES = {
  PLAYER: 1,
  MAKER: 2,
  UNLIMITED_MAKER: 4,
  ADMIN: 8,
  CREATOR: 16,
  SUPER_ADMIN: 32,
}