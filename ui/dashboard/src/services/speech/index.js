import { getDefaultVoice, isValidVoice } from "./voice";

const { loadVoice, speak } = window.meSpeak

export const avatarSpeak = (avatar, message = avatar.speak.message) => {
    const params = {}
    if (avatar.voice) {
        const { voice, variant, amplitude, pitch, speed } = avatar.voice
        params.variant = variant
        params.amplitude = amplitude
        params.pitch = pitch
        params.speed = speed;
        const callback = () => speak(cleanEmoji(message), params) // voice got loaded assynchronous
        if (isValidVoice(voice)) {
            loadVoice(voice, callback)
        } else {
            loadVoice(getDefaultVoice(), callback)
        }
    }

}

export const cleanEmoji = message => {
    return message.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '');
}