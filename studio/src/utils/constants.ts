// @ts-nocheck
export const TOPICS = {
  CHAT: "chat",
  BOARD: "board",
  BACKGROUND: "background",
  AUDIO: "audio",
  REACTION: "reaction",
  COUNTER: "counter",
  DRAW: "draw",
  STATISTICS: "statistics",
};

export const BOARD_ACTIONS = {
  PLACE_OBJECT_ON_STAGE: "placeObjectOnStage",
  MOVE_TO: "moveTo",
  DESTROY: "destroy",
  SWITCH_FRAME: "switchFrame",
  SPEAK: "speak",
  SEND_TO_BACK: "sendToBack",
  BRING_TO_FRONT: "bringToFront",
  BRING_TO_FRONT_OF: "bringToFrontOf",
  TOGGLE_AUTOPLAY_FRAMES: "toggleAutoplayFrames",
};

export const BACKGROUND_ACTIONS = {
  CHANGE_BACKGROUND: "changeBackground",
  SET_CHAT_VISIBILITY: "setChatVisibility",
  SET_REACTION_VISIBILITY: "setReactionVisibility",
  CLEAR_CHAT: "clearChat",
  SET_CHAT_POSITION: "setChatPosition",
  SET_BACKDROP_COLOR: "setBackdropColor",
  DRAW_CURTAIN: "drawCurtain",
  LOAD_SCENES: "loadScenes",
  SWITCH_SCENE: "switchScene",
  BLANK_SCENE: "blankScene",
  SET_DARK_MODE_CHAT: "setDarkModeChat",
};

export const DRAW_ACTIONS = {
  NEW_LINE: "newLine",
  UNDO: "undo",
  CLEAR: "clear",
};

export const ROLES = {
  GUEST: 4,
  PLAYER: 1,
  ADMIN: 8,
  SUPER_ADMIN: 32,
};

export const UPDATE_LIMIT = {
  1: 1024 * 1024,
  2: 1024 * 1024 * 2,
  5: 1024 * 1024 * 5,
  10: 1024 * 1024 * 10,
};

export const COLORS = {
  DEFAULT_BACKDROP: "#30ac45",
};

export const MEDIA_COPYRIGHT_LEVELS = [
  {
    value: 0,
    name: "✅ Copyright free",
    description:
      "Can be used by other players in any way without need for permission",
  },
  {
    value: 1,
    name: "👌 Use with acknowledgement",
    description:
      "Other players can use the media item as long as the owner is acknowledged",
  },
  {
    value: 2,
    name: "🔑 Use with permission",
    description:
      "Other players must ask the owner for permission if they want to use the media item",
  },
  {
    value: 3,
    name: "🔒️ Not shared",
    description:
      "Only the owner can assign this media item to a stage. Once it is assigned to a stage it can be used there by players who have access to that stage.",
  },
];

export const imageExtensions = ".svg,.jpg,.jpeg,.png,.gif";
export const audioExtensions =
  ".wav,.mpeg,.mp3,.aac,.aacp,.ogg,.webm,.flac,.m4a";
export const videoExtensions = ".mp4,.webm,.opgg,.3gp,.flv";
export const orderTitle = [
  {
    label: "Newest",
    value: (a, b) => {
      return new Date(b.createdOn) - new Date(a.createdOn);
    },
  },
  {
    label: "Latest",
    value: (a, b) => {
      return new Date(a.createdOn) - new Date(b.createdOn);
    },
  },
  {
    label: "A → Z",
    value: (a, b) => {
      let fa = a.name.toLowerCase();
      let fb = b.name.toLowerCase();

      if (fa < fb) {
        return -1;
      }
      if (fa > fb) {
        return 1;
      }
      return 0;
    },
  },
  {
    label: "Z ← A",
    value: (a, b) => {
      let fa = a.name.toLowerCase();
      let fb = b.name.toLowerCase();

      if (fa > fb) {
        return -1;
      }
      if (fa < fb) {
        return 1;
      }
      return 0;
    },
  },
];
