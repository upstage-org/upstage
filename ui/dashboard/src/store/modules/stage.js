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
                .concat(state.tools.props.map(p => p.src))
                .concat(state.tools.backdrops.map(b => b.src))
            return assets;
        },
        audios(state) {
            return state.tools.audios;
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
        sendChat({ rootGetters, state }, message) {
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
        handleBoardMessage({ commit }, { message }) {
            switch (message.type) {
                case BOARD_ACTIONS.PLACE_AVATAR_ON_STAGE:
                    commit('PUSH_AVATARS', message.avatar)
                    break;
                case BOARD_ACTIONS.MOVE_TO:
                    commit('UPDATE_OBJECT', message.object)
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
