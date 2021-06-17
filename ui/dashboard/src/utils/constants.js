export const TOPICS = {
  CHAT: "chat",
  BOARD: "board",
  BACKGROUND: "background",
  AUDIO: "audio",
  REACTION: "reaction",
  COUNTER: "counter",
  STATISTICS: "statistics",
}

export const BOARD_ACTIONS = {
  PLACE_OBJECT_ON_STAGE: 'placeObjectOnStage',
  MOVE_TO: 'moveTo',
  DESTROY: 'destroy',
  SWITCH_FRAME: 'switchFrame',
  SPEAK: 'speak',
  SEND_TO_BACK: 'sendToBack',
  BRING_TO_FRONT: 'bringToFront',
  BRING_TO_FRONT_OF: 'bringToFrontOf',
  TOGGLE_AUTOPLAY_FRAMES: 'toggleAutoplayFrames',
}

export const BACKGROUND_ACTIONS = {
  CHANGE_BACKGROUND: 'changeBackground',
  SET_CHAT_VISIBILITY: 'setChatVisibility',
  SET_BACKDROP_COLOR: 'setBackdropColor'
}

export const ROLES = {
  PLAYER: 1,
  MAKER: 2,
  GUEST: 4,
  ADMIN: 8,
  CREATOR: 16,
  SUPER_ADMIN: 32,
}
