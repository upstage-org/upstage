import moment from 'moment'
import { v4 as uuidv4 } from "uuid";
import mqtt from '@/services/mqtt'
import { isJson, randomMessageColor } from '@/utils/common'
import { generateDemoData } from '../demoData'
import { TOPICS, BOARD_ACTIONS } from '@/utils/constants'

export default {
    namespaced: true,
    state: {
        preloading: true,
        background: null,
        status: 'OFFLINE',
        subscribeSuccess: false,
        chat: {
            messages: [],
            color: randomMessageColor(),
        },
        board: {
            avatars: [],
        },
        tools: generateDemoData(),
        settingPopup: {
            isActive: false,
        }
    },
    getters: {
        avatars(state) {
            return state.board.avatars;
        },
        config(state) {
            return state.tools.config;
        },
        preloadableAssets(state) {
            const assets = []
                .concat(state.tools.avatars.map(a => a.src))
                .concat(state.tools.avatars.map(a => a.frames ?? []).flat())
                .concat(state.tools.props.map(p => p.src))
                .concat(state.tools.backdrops.map(b => b.src))
            return assets;
        },
        audios(state) {
            return state.tools.audios;
        },
        currentAvatar(state, getters, rootState) {
            const id = rootState.user.avatarId;
            return state.board.avatars.find(avatar => avatar.id === id);
        }
    },
    mutations: {
        SET_BACKGROUND(state, background) {
            state.background = background
        },
        SET_STATUS(state, status) {
            state.status = status
        },
        SET_SUBSCRIBE_STATUS(state, status) {
            state.subscribeSuccess = status
        },
        PUSH_CHAT_MESSAGE(state, message) {
            state.chat.messages.push(message)
        },
        PUSH_AVATARS(state, avatar) {
            state.board.avatars.push(avatar)
        },
        UPDATE_OBJECT(state, object) {
            const { id } = object;
            const avatar = state.board.avatars.find(avatar => avatar.id === id);
            if (avatar) { // Object an is avatar
                Object.assign(avatar, object);
                return;
            }
            state.board.avatars.push(object)
        },
        DELETE_OBJECT(state, object) {
            const { id } = object;
            state.board.avatars = state.board.avatars.filter(avatar => avatar.id !== id);
        },
        SET_OBJECT_SPEAK(state, { avatar, speak }) {
            const { id } = avatar;
            let model = state.board.avatars.find(avatar => avatar.id === id);
            if (!model) {
                const length = state.board.avatars.push(avatar)
                model = state.board.avatars[length - 1];
            }
            model.speak = speak;
            setTimeout(() => {
                if (model.speak.message === speak.message) { model.speak = null }
            }, 1000 + speak.message.split(' ').length * 1000);
        },
        SET_PRELOADING_STATUS(state, status) {
            state.preloading = status;
        },
        UPDATE_AUDIO(state, audio) {
            const model = state.tools.audios.find(a => a.src === audio.src);
            if (model) {
                Object.assign(model, audio);
            }
        },
        SET_SETTING_POPUP(state, setting) {
            state.settingPopup = setting;
        },
        BRING_TO_FRONT(state, object) {
            const index = state.board.avatars.findIndex(avatar => avatar.id === object.id);
            if (index > -1) {
                state.board.avatars.push(state.board.avatars.splice(index, 1)[0]);
            } else {
                state.board.avatars.push(object)
            }
        },
        SEND_TO_BACK(state, object) {
            const index = state.board.avatars.findIndex(avatar => avatar.id === object.id);
            if (index > -1) {
                state.board.avatars.unshift(state.board.avatars.splice(index, 1)[0]);
            } else {
                state.board.avatars.push(object)
            }
        }
    },
    actions: {
        connect({ commit, dispatch }) {
            commit('SET_STATUS', 'CONNECTING')

            const client = mqtt.connect();
            client.on("connect", () => {
                console.log("Connection succeeded!");
                commit('SET_STATUS', 'LIVE')
                dispatch('subscribe');
            });
            client.on("error", (error) => {
                console.log(error);
                commit('SET_STATUS', 'OFFLINE')
            });
            client.on("message", (topic, rawMessage) => {
                const decoded = new TextDecoder().decode(new Uint8Array(rawMessage));
                const message = (isJson(decoded) && JSON.parse(decoded)) || decoded;
                dispatch('handleMessage', { topic, message });
            });
        },
        subscribe({ commit }) {
            const topics = {
                [TOPICS.CHAT]: { qos: 2 },
                [TOPICS.BOARD]: { qos: 2 },
                [TOPICS.BACKGROUND]: { qos: 2 },
                [TOPICS.AUDIO]: { qos: 2 },
            }
            mqtt.subscribe(topics).then(res => {
                commit('SET_SUBSCRIBE_STATUS', true)
                console.log("Subscribed to topics: ", res);
            })
        },
        disconnect() {
            mqtt.disconnect();
        },
        handleMessage({ dispatch }, { topic, message }) {
            switch (topic) {
                case TOPICS.CHAT:
                    dispatch('handleChatMessage', { message });
                    break;
                case TOPICS.BOARD:
                    dispatch('handleBoardMessage', { message });
                    break;
                case TOPICS.BACKGROUND:
                    dispatch('handleBackgroundMessage', { message });
                    break;
                case TOPICS.AUDIO:
                    dispatch('handleAudioMessage', { message });
                    break;
                default:
                    break;
            }
        },
        sendChat({ rootGetters, state, getters }, message) {
            if (!message) return;
            const nickname = rootGetters["user/nickname"];
            const payload = {
                user: nickname,
                message: message,
                color: state.chat.color.text,
                backgroundColor: state.chat.color.bg,
                at: moment().format('HH:mm')
            };
            mqtt.sendMessage(TOPICS.CHAT, payload).catch(error => console.log(error));
            const avatar = getters['currentAvatar']
            if (avatar) {
                mqtt.sendMessage(TOPICS.BOARD, {
                    type: BOARD_ACTIONS.SPEAK,
                    avatar,
                    speak: payload,
                })
            }
        },
        handleChatMessage({ commit }, { message }) {
            const model = {
                user: 'Anonymous',
                color: "#000000"
            };
            if (typeof message === "object") {
                Object.assign(model, message)
            } else {
                model.message = message;
            }
            commit('PUSH_CHAT_MESSAGE', model)
        },
        summonAvatar(action, avatar) {
            const payload = {
                type: BOARD_ACTIONS.PLACE_AVATAR_ON_STAGE,
                avatar: {
                    id: uuidv4(),
                    ...avatar,
                    w: 100,
                    h: 100,
                    opacity: 1,
                }
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        shapeObject(action, object) {
            const payload = {
                type: BOARD_ACTIONS.MOVE_TO,
                object,
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        deleteObject(action, object) {
            const payload = {
                type: BOARD_ACTIONS.DESTROY,
                object,
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        switchFrame(action, object) {
            const payload = {
                type: BOARD_ACTIONS.SWITCH_FRAME,
                object,
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        bringToFront(action, object) {
            const payload = {
                type: BOARD_ACTIONS.BRING_TO_FRONT,
                object,
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        sendToBack(action, object) {
            const payload = {
                type: BOARD_ACTIONS.SEND_TO_BACK,
                object,
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        handleBoardMessage({ commit }, { message }) {
            switch (message.type) {
                case BOARD_ACTIONS.PLACE_AVATAR_ON_STAGE:
                    commit('PUSH_AVATARS', message.avatar);
                    break;
                case BOARD_ACTIONS.MOVE_TO:
                    commit('UPDATE_OBJECT', message.object);
                    commit('BRING_TO_FRONT', message.object);
                    break;
                case BOARD_ACTIONS.DESTROY:
                    commit('DELETE_OBJECT', message.object);
                    break;
                case BOARD_ACTIONS.SWITCH_FRAME:
                    commit('UPDATE_OBJECT', message.object);
                    commit('BRING_TO_FRONT', message.object);
                    break;
                case BOARD_ACTIONS.SPEAK:
                    commit('SET_OBJECT_SPEAK', message);
                    break;
                case BOARD_ACTIONS.BRING_TO_FRONT:
                    commit('BRING_TO_FRONT', message.object);
                    break;
                case BOARD_ACTIONS.SEND_TO_BACK:
                    commit('SEND_TO_BACK', message.object);
                    break;
                default:
                    break;
            }
        },
        setBackground(action, background) {
            mqtt.sendMessage(TOPICS.BACKGROUND, background)
        },
        handleBackgroundMessage({ commit }, { message }) {
            commit('SET_BACKGROUND', message);
        },
        playAudio(_, audio) {
            audio.isPlaying = true;
            mqtt.sendMessage(TOPICS.AUDIO, audio)
        },
        pauseAudio(_, audio) {
            audio.isPlaying = false;
            mqtt.sendMessage(TOPICS.AUDIO, audio)
        },
        handleAudioMessage({ commit }, { message }) {
            commit('UPDATE_AUDIO', message)
        },
        closeSettingPopup({ commit }) {
            commit('SET_SETTING_POPUP', { isActive: false })
        },
        openSettingPopup({ commit }, setting) {
            setting.isActive = true;
            commit('SET_SETTING_POPUP', setting)
        },
    },
};
