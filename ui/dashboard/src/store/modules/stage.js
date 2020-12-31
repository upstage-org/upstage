import moment from 'moment'
import mqtt from '@/services/mqtt'
import { isJson, randomMessageColor } from '@/utils/common'

export default {
    namespaced: true,
    state: {
        background: null,
        status: 'OFFLINE',
        subscribeSuccess: false,
        chat: {
            messages: [],
            color: randomMessageColor(),
        }
    },
    getters: {
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
        PUSH_MESSAGE(state, message) {
            state.chat.messages.push(message)
        }
    },
    actions: {
        setBackground({ commit }, background) {
            commit('SET_BACKGROUND', background);
        },
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
            client.on("message", (topic, message) => {
                dispatch('handleMessage', { topic, message });
            });
        },
        subscribe({ commit }) {
            mqtt.subscribe().then(res => {
                commit('SET_SUBSCRIBE_STATUS', true)
                console.log("Subscribed to topics: ", res);
            })
        },
        handleMessage({ commit }, { topic, message }) {
            const arr = new TextDecoder().decode(new Uint8Array(message));

            if (topic === "topic/commands") {
                const convertedMessage = (isJson(arr) && JSON.parse(arr)) || arr;
                const modelMessage = {
                    user: 'Anonymous',
                    color: "#000000"
                };
                if (typeof convertedMessage === "object") {
                    Object.assign(modelMessage, convertedMessage)
                } else {
                    modelMessage.message = convertedMessage;
                }
                commit('PUSH_MESSAGE', modelMessage)
            } else if (topic === "topic/board") {
                this.addShape(arr);
            }
        },
        sendMessage({ rootGetters, state }, message) {
            if (!message) return;
            const currentUser = rootGetters["user/currentUser"];
            const messageModel = {
                user: currentUser,
                message: message,
                color: state.chat.color.text,
                backgroundColor: state.chat.color.bg,
                at: moment().format('HH:mm')
            };
            const converted = JSON.stringify(messageModel);
            mqtt.publish(converted).catch(error => console.log(error));
        }
    },
};
