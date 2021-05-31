import { getDefaultVoice, isValidVoice } from "./voice";

const { loadVoice, speak } = window.meSpeak

export const avatarSpeak = (avatar, message = avatar.speak.message) => {
    const params = {}
    const callback = () => speak(message, params) // voice got loaded assynchronous
    if (avatar.voice) {
        console.log(avatar.voice)
        const { voice, variant, amplitude, pitch, speed } = avatar.voice
        if (isValidVoice(voice)) {
            loadVoice(voice, callback)
        } else {
            loadVoice(getDefaultVoice(), callback)
        }
        params.variant = variant
        params.amplitude = amplitude
        params.pitch = pitch
        params.speed = speed;
    }

}
