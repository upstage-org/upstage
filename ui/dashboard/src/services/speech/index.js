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
        const callback = () => speak(message, params) // voice got loaded assynchronous
        if (isValidVoice(voice)) {
            loadVoice(voice, callback)
        } else {
            loadVoice(getDefaultVoice(), callback)
        }
    }

}
