export const avatarSpeak = avatar => {
    speechSynthesis.cancel()
    let utterance = new SpeechSynthesisUtterance(avatar.speak.message);
    speechSynthesis.speak(utterance);
}
