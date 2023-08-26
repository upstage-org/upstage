import { AvatarVoice } from "models/studio";
import { getDefaultVoice, isValidVoice } from "./voice";

const { loadVoice, speak, stop } = (window as any).meSpeak;

export const avatarSpeak = (voice: AvatarVoice, message: string) => {
  if (voice.voice) {
    const callback = () => {
      speak(cleanEmoji(message), voice);
    }; // voice got loaded assynchronous
    if (isValidVoice(voice.voice)) {
      loadVoice(voice.voice, callback);
    } else {
      loadVoice(getDefaultVoice(), callback);
    }
  }
};

export const stopSpeaking = stop;

export const cleanEmoji = (message: string) => {
  return message.replace(
    /([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g,
    "",
  );
};
