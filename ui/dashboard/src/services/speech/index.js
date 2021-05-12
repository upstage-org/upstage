import { getDefaultVoice, isValidVoice } from "./voice";

const { loadVoice, speak } = window.meSpeak

export const avatarSpeak = (avatar, message = avatar.speak.message) => {
    const params = {}
    if (avatar.voice) {
        const { voice, variant, amplitude, pitch, speed } = avatar.voice
        if (isValidVoice(voice)) {
            loadVoice(voice)
        } else {
            loadVoice(getDefaultVoice())
        }
        params.variant = variant
        params.amplitude = amplitude
        params.pitch = pitch
        params.speed = speed;
    }
    speak(message, params)
}
