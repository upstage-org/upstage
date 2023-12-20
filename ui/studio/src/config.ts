import { getSharedConfig } from "./utils/common"

const configs = {
  MODE: import.meta.env.MODE as 'development' | 'production',
  UPSTAGE_URL: window.location.origin,
  SHARED: getSharedConfig(),
  ALLOWED_EXTENSIONS: {
    IMAGE: '.svg,.jpg,.jpeg,.png,.gif',
    AUDIO: '.wav,.mpeg,.mp3,.aac,.aacp,.ogg,.webm,.flac,.m4a',
    VIDEO: '.mp4,.webm,.opgg,.3gp,.flv'
  },
  ROLES: {
    GUEST: 4,
    PLAYER: 1,
    ADMIN: 8,
    SUPER_ADMIN: 32,
  },
  MEDIA_COPYRIGHT_LEVELS: [
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
      name: "🔐 Use with permission",
      description:
        "Other players must ask the owner for permission if they want to use the media item",
    },
    {
      value: 3,
      name: "🔒️ Not shared",
      description:
        "Only the owner can assign this media item to a stage. Once it is assigned to a stage it can be used there by players who have access to that stage.",
    },
  ],
}

export default configs
