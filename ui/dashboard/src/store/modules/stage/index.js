import moment from 'moment'
import { v4 as uuidv4 } from "uuid";
import hash from 'object-hash';
import buildClient from '@/services/mqtt'
import { absolutePath, cloneDeep, randomColor, randomMessageColor, randomRange } from '@/utils/common'
import { TOPICS, BOARD_ACTIONS, BACKGROUND_ACTIONS } from '@/utils/constants'
import { deserializeObject, recalcFontSize, serializeObject, unnamespaceTopic, getDefaultStageConfig } from './reusable';
import { getViewport } from './reactiveViewport';
import { stageGraph } from '@/services/graphql';
import { useAttribute } from '@/services/graphql/composable';
import { avatarSpeak } from '@/services/speech';
import { nmsService } from "@/services/rest";
import anime from 'animejs';

const mqtt = buildClient()

export default {
    namespaced: true,
    state: {
        preloading: true,
        model: null,
        background: null,
        curtain: null,
        backdropColor: '#ebffee',
        status: 'OFFLINE',
        subscribeSuccess: false,
        activeMovable: null,
        chat: {
            messages: [],
            color: randomMessageColor(),
            opacity: 0.9,
            fontSize: '14px',
        },
        board: {
            objects: [],
            drawings: [],
            texts: [],
        },
        tools: {
            avatars: [],
            props: [],
            backdrops: [],
            audios: [],
            streams: [],
            shapes: [],
            curtains: [],
            config: getDefaultStageConfig(),
        },
        settingPopup: {
            isActive: false,
        },
        preferences: {
            isDrawing: true,
            text: {
                fontSize: '20px',
                fontFamily: 'Josefin Sans',
            }
        },
        settings: {
            chatVisibility: true,
        },
        hosts: [],
        reactions: [],
        viewport: getViewport(),
        sessions: [],
        session: null,
        replay: {
            timestamp: {
                begin: 0,
                end: 0,
                current: 0
            },
            timers: [],
            interval: null,
            speed: 32
        },
        loadingRunningStreams: false,
        audioPlayers: [],
        scenes: []
    },
    getters: {
        ready(state) {
            return state.model && !state.preloading;
        },
        url(state) {
            return state.model ? state.model.fileLocation : 'demo';
        },
        objects(state) {
            return state.board.objects.map(o => ({
                ...o,
                holder: state.sessions.find((s) => s.avatarId === o.id)
            }));
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
                .concat(state.tools.shapes.map(b => b.src))
                .concat(state.tools.curtains.map(b => b.src))
            return assets;
        },
        audios(state) {
            return state.tools.audios;
        },
        currentAvatar(state, getters, rootState) {
            const id = rootState.user.avatarId;
            return state.board.objects.find(o => o.id === id);
        },
        stageSize(state, getters) {
            let width = state.viewport.width;
            let height = state.viewport.height;
            let left = 0;
            let top = 0;
            const ratio = getters.config.ratio;
            if (width / height > ratio) {
                width = height * ratio;
                left = (window.innerWidth - width) / 2;
            } else {
                height = width / ratio;
                top = (window.innerHeight - height) / 2;
            }
            return { width, height, left, top };
        },
        canPlay(state) {
            return state.model.permission && state.model.permission !== 'audience'
        },
        players(state) {
            return state.sessions.filter((s) => s.isPlayer)
        },
        audiences(state) {
            return state.sessions.filter((s) => !s.isPlayer)
        }
    },
    mutations: {
        SET_MODEL(state, model) {
            state.model = model
            if (model) {
                const media = model.media;
                if (media && media.length) {
                    media.forEach(item => {
                        if (item.description) {
                            const meta = JSON.parse(item.description)
                            delete item.description
                            Object.assign(item, meta)
                        }
                        if (item.type === 'stream') {
                            if (item.isRTMP) {
                                item.url = item.src
                            } else {
                                item.url = absolutePath(item.src);
                            }
                            delete item.src
                        } else {
                            item.src = absolutePath(item.src);
                        }
                        if (item.multi) {
                            item.frames = item.frames.map(src => absolutePath(src))
                        }
                        const key = item.type + 's';
                        if (!state.tools[key]) {
                            state.tools[key] = [];
                        }
                        state.tools[key].push(item)
                    });
                } else {
                    state.preloading = false;
                }
                const config = useAttribute({ value: model }, 'config', true).value;
                if (config) {
                    Object.assign(state.tools.config, config)
                    state.tools.config.ratio = config.ratio.width / config.ratio.height
                }
                const cover = useAttribute({ value: model }, 'cover', false).value;
                state.model.cover = cover && absolutePath(cover)
            }
        },
        CLEAN_STAGE(state, cleanModel) {
            if (cleanModel) {
                state.model = null;
            }
            state.status = 'OFFLINE';
            if (state.background?.interval) {
                clearInterval(state.background.interval);
            }
            state.background = null;
            state.tools.avatars = [];
            state.tools.props = [];
            state.tools.backdrops = []
            state.tools.audios = []
            state.tools.streams = [];
            state.tools.config = getDefaultStageConfig()
            state.board.objects = [];
            state.board.drawings = [];
            state.board.texts = [];
            state.chat.messages = [];
            state.chat.color = randomColor();
        },
        SET_BACKGROUND(state, background) {
            if (background) {
                if (!state.background || !state.background.at || (state.background.at < background.at)) {
                    if (state.background?.interval) {
                        clearInterval(state.background.interval);
                    }
                    state.background = background
                    anime({
                        targets: "#board",
                        opacity: [0, 1],
                        duration: 5000,
                    });
                    if (background.multi && background.speed > 0) {
                        const { speed, frames } = state.background;
                        state.background.interval = setInterval(() => {
                            let nextFrame = frames.indexOf(state.background.currentFrame) + 1;
                            if (nextFrame >= frames.length) {
                                nextFrame = 0;
                            }
                            state.background.currentFrame = frames[nextFrame];
                        }, 50 / speed);
                    }
                }
            }
        },
        SET_STATUS(state, status) {
            state.status = status
        },
        SET_SUBSCRIBE_STATUS(state, status) {
            state.subscribeSuccess = status
        },
        PUSH_CHAT_MESSAGE(state, message) {
            message.hash = hash(message)
            const lastMessage = state.chat.messages[state.chat.messages.length - 1]
            if (lastMessage && (lastMessage.hash === message.hash)) {
                return
            }
            state.chat.messages.push(message)
        },
        CLEAR_CHAT(state) {
            state.chat.messages.length = 0
        },
        PUSH_OBJECT(state, object) {
            const { id } = object;
            deserializeObject(object);
            const model = state.board.objects.find(o => o.id === id);
            if (model) {
                Object.assign(model, object);
            } else {
                state.board.objects.push(object)
            }
        },
        UPDATE_OBJECT(state, object) {
            const { id } = object;
            deserializeObject(object);
            const model = state.board.objects.find(o => o.id === id);
            if (model) {
                const deltaX = object.x - model.x
                const deltaY = object.y - model.y
                const deltaW = object.w / model.w
                const deltaH = object.h / model.h
                const deltaRotate = object.rotate - model.rotate
                const costumes = state.board.objects.filter(o => o.wornBy === id)
                if (costumes.length) {
                    costumes.forEach(costume => {
                        costume.moveSpeed = object.moveSpeed
                        costume.opacity = object.opacity
                        costume.liveAction = object.liveAction
                        const offsetX = costume.x - model.x
                        const offsetY = costume.y - model.y
                        costume.x += deltaX + offsetX * deltaW - offsetX
                        costume.y += deltaY + offsetY * deltaH - offsetY
                        costume.w *= deltaW
                        costume.h *= deltaH
                        costume.rotate += deltaRotate
                    })
                }
                Object.assign(model, object);
            }
        },
        DELETE_OBJECT(state, object) {
            const { id } = object;
            state.board.objects = state.board.objects.filter(o => o.id !== id);
            state.board.objects.filter(o => o.wornBy === id).forEach(costume => {
                costume.wornBy = null
            })
        },
        SET_OBJECT_SPEAK(state, { avatar, speak }) {
            const { id } = avatar;
            let model = state.board.objects.find(o => o.id === id);
            if (model) {
                speak.hash = hash(speak)
                if (model.speak?.hash !== speak.hash) {
                    model.speak = speak;
                    if (state.status === 'LIVE' || state.replay.isReplaying) {
                        avatarSpeak(model);
                    }
                    setTimeout(() => {
                        if (model.speak?.message === speak.message) { model.speak = null }
                    }, 1000 + speak.message.split(' ').length * 1000);
                }
            }
        },
        SET_PRELOADING_STATUS(state, status) {
            state.preloading = status;
        },
        UPDATE_AUDIO(state, audio) {
            const model = state.tools.audios.find(a => a.src === audio.src);
            if (model) {
                audio.changed = true
                Object.assign(model, audio);
            }
        },
        SET_SETTING_POPUP(state, setting) {
            state.settingPopup = setting;
        },
        SEND_TO_BACK(state, object) {
            const index = state.board.objects.findIndex(avatar => avatar.id === object.id);
            if (index > -1) {
                state.board.objects.unshift(state.board.objects.splice(index, 1)[0]);
            }
        },
        BRING_TO_FRONT(state, object) {
            const index = state.board.objects.findIndex(avatar => avatar.id === object.id);
            if (index > -1) {
                state.board.objects.push(state.board.objects.splice(index, 1)[0]);
            }
        },
        BRING_TO_FRONT_OF(state, { front, back }) {
            const frontIndex = state.board.objects.findIndex(avatar => avatar.id === front);
            const backIndex = state.board.objects.findIndex(avatar => avatar.id === back);
            if (frontIndex > -1 && backIndex > -1) {
                state.board.objects.splice(backIndex, 0, state.board.objects.splice(frontIndex, 1)[0])
            }
        },
        SET_PREFERENCES(state, preferences) {
            Object.assign(state.preferences, preferences);
        },
        PUSH_DRAWING(state, drawing) {
            state.board.drawings.push(cloneDeep(drawing));
        },
        PUSH_TEXT(state, text) {
            state.board.texts.push(text);
        },
        PUSH_STREAM_TOOL(state, stream) {
            state.tools.streams.push(stream);
        },
        PUSH_STREAM_HOST(state, stream) {
            state.hosts.push(stream);
        },
        PUSH_RUNNING_STREAMS(state, streams) {
            state.tools.streams = state.tools.streams.filter(s => !s.autoDetect).concat(streams);
        },
        PUSH_SHAPES(state, shapes) {
            state.tools.shapes = shapes;
        },
        PUSH_CURTAINS(state, curtains) {
            state.tools.curtains = curtains;
        },
        UPDATE_IS_DRAWING(state, isDrawing) {
            state.preferences.isDrawing = isDrawing;
        },
        UPDATE_IS_WRITING(state, isWriting) {
            state.preferences.isWriting = isWriting;
        },
        UPDATE_TEXT_OPTIONS(state, options) {
            Object.assign(state.preferences.text, options);
        },
        PUSH_REACTION(state, reaction) {
            state.reactions.push({
                reaction,
                x: randomRange(150, window.innerWidth) - 300,
                y: window.innerHeight - 100,
            });
            setTimeout(() => {
                state.reactions.shift();
            }, state.tools.config.reactionDuration);
        },
        UPDATE_VIEWPORT(state, viewport) {
            state.viewport = viewport;
        },
        RESCALE_OBJECTS(state, ratio) {
            state.board.objects.forEach(object => {
                object.x = object.x * ratio;
                object.y = object.y * ratio;
                object.w = object.w * ratio;
                object.h = object.h * ratio;
                recalcFontSize(object, s => s * ratio)
            })
        },
        SET_CHAT_PARAMETERS(state, { opacity, fontSize }) {
            state.chat.opacity = opacity;
            state.chat.fontSize = fontSize;
        },
        UPDATE_SESSIONS_COUNTER(state, session) {
            const index = state.sessions.findIndex(s => s.id === session.id)
            if (index > -1) {
                if (session.leaving) {
                    return state.sessions.splice(index, 1)
                } else {
                    Object.assign(state.sessions[index], session)
                }
            } else {
                state.sessions.push(session)
            }
            state.sessions = state.sessions.filter(s => moment().diff(moment(new Date(s.at)), 'minute') < 60);
            state.sessions.sort((a, b) => b.at - a.at);
        },
        SET_CHAT_VISIBILITY(state, visible) {
            state.settings.chatVisibility = visible
        },
        SET_BACKDROP_COLOR(state, color) {
            state.backdropColor = color
        },
        SET_REPLAY(state, replay) {
            Object.assign(state.replay, replay)
        },
        SET_ACTIVE_MOVABLE(state, id) {
            state.activeMovable = id
        },
        UPDATE_AUDIO_PLAYER_STATUS(state, { index, ...status }) {
            if (!state.audioPlayers[index]) {
                state.audioPlayers[index] = {}
            }
            Object.assign(state.audioPlayers[index], status)
        },
        SET_CURTAIN(state, curtain) {
            state.curtain = curtain
        },
        REPLACE_SCENE(state, { payload }) {
            anime({
                targets: "#live-stage",
                filter: ['brightness(0)', 'brightness(1)'],
                easing: 'linear',
                duration: 3000
            });
            state.activeMovable = null
            const snapshot = JSON.parse(payload)
            snapshot.board.objects.forEach(deserializeObject)
            Object.keys(snapshot).forEach(key => {
                state[key] = snapshot[key]
            })
        }
    },
    actions: {
        connect({ commit, dispatch }) {
            commit('SET_STATUS', 'CONNECTING')

            const client = mqtt.connect();
            client.on("connect", () => {
                commit('SET_STATUS', 'LIVE')
                dispatch('subscribe');
                dispatch('joinStage');
            });
            client.on("error", () => {
                commit('SET_STATUS', 'OFFLINE')
            });
            mqtt.receiveMessage((payload) => {
                dispatch('handleMessage', payload);
            })
        },
        subscribe({ commit, dispatch }) {
            const topics = {
                [TOPICS.CHAT]: { qos: 2 },
                [TOPICS.BOARD]: { qos: 2 },
                [TOPICS.BACKGROUND]: { qos: 2 },
                [TOPICS.AUDIO]: { qos: 2 },
                [TOPICS.REACTION]: { qos: 2 },
                [TOPICS.COUNTER]: { qos: 2 },
            }
            mqtt.subscribe(topics).then(res => {
                commit('SET_SUBSCRIBE_STATUS', true);
                console.log("Subscribed to topics: ", res);
                dispatch('sendStatistics')
            })
        },
        async disconnect({ dispatch }) {
            await dispatch('leaveStage', true);
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
                case TOPICS.REACTION:
                    dispatch('handleReactionMessage', { message });
                    break;
                case TOPICS.COUNTER:
                    dispatch('handleCounterMessage', { message });
                    break;
                default:
                    break;
            }
        },
        sendChat({ rootGetters, getters }, message) {
            if (!message) return;
            let user = rootGetters["user/chatname"];
            let isPlayer = getters["canPlay"]
            let behavior = "speak"
            if (message.startsWith(":")) {
                behavior = "think";
                message = message.substr(1)
            }
            if (message.startsWith("!")) {
                behavior = "shout"
                message = message.substr(1).toUpperCase()
            }
            if (isPlayer && message.startsWith("-")) {
                message = message.substr(1)
                const fakeName = message.split(' ')[0]
                if (fakeName) {
                    user = fakeName
                    message = message.substr(fakeName.length).trim()
                }
                isPlayer = false
            }
            const payload = {
                user,
                message: message,
                behavior,
                isPlayer,
                at: +new Date()
            };
            mqtt.sendMessage(TOPICS.CHAT, payload);
            const avatar = getters['currentAvatar']
            if (avatar && isPlayer) {
                mqtt.sendMessage(TOPICS.BOARD, {
                    type: BOARD_ACTIONS.SPEAK,
                    avatar,
                    speak: payload,
                })
            }
        },
        handleChatMessage({ commit }, { message }) {
            if (message.clear) {
                commit('CLEAR_CHAT')
            } else {
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
            }
        },
        placeObjectOnStage({ commit, dispatch }, data) {
            const object = {
                w: 100,
                h: 100,
                opacity: 1,
                moveSpeed: 2000,
                voice: {},
                rotate: 0,
                ...data,
                id: uuidv4(),
            }
            commit('PUSH_OBJECT', serializeObject(object));
            if (object.type === 'stream') {
                commit('PUSH_STREAM_HOST', object);
            }
            if (data.type === 'avatar' || data.type === 'drawing') {
                dispatch("user/setAvatarId", object.id, { root: true }).then(() => {
                    commit("SET_ACTIVE_MOVABLE", null)
                });
            }
            return object;
        },
        shapeObject({ commit, state }, object) {
            if (object.liveAction) {
                if (object.published) {
                    mqtt.sendMessage(TOPICS.BOARD, {
                        type: BOARD_ACTIONS.MOVE_TO,
                        object: serializeObject(object)
                    })
                } else {
                    object.published = true
                    mqtt.sendMessage(TOPICS.BOARD, {
                        type: BOARD_ACTIONS.PLACE_OBJECT_ON_STAGE,
                        object: serializeObject(object)
                    })
                }
                state.board.objects.filter(o => o.wornBy === object.id).forEach(costume => {
                    if (!costume.published) {
                        costume.published = true
                        mqtt.sendMessage(TOPICS.BOARD, {
                            type: BOARD_ACTIONS.PLACE_OBJECT_ON_STAGE,
                            object: serializeObject(costume)
                        })
                    }
                })
            } else {
                commit('UPDATE_OBJECT', serializeObject(object))
            }
        },
        deleteObject(action, object) {
            object = serializeObject(object)
            if (object.type === 'drawing') {
                delete object.commands
            }
            const payload = {
                type: BOARD_ACTIONS.DESTROY,
                object
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        switchFrame(action, object) {
            const payload = {
                type: BOARD_ACTIONS.SWITCH_FRAME,
                object: serializeObject(object),
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        sendToBack(action, object) {
            const payload = {
                type: BOARD_ACTIONS.SEND_TO_BACK,
                object: serializeObject(object)
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        bringToFront(action, object) {
            const payload = {
                type: BOARD_ACTIONS.BRING_TO_FRONT,
                object: serializeObject(object)
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        bringToFrontOf(action, { front, back }) {
            const payload = {
                type: BOARD_ACTIONS.BRING_TO_FRONT_OF,
                front,
                back
            }
            mqtt.sendMessage(TOPICS.BOARD, payload)
        },
        toggleAutoplayFrames(action, object) {
            const payload = {
                type: BOARD_ACTIONS.TOGGLE_AUTOPLAY_FRAMES,
                object: serializeObject(object),
            }
            mqtt.sendMessage(TOPICS.BOARD, payload);
        },
        handleBoardMessage({ commit }, { message }) {
            switch (message.type) {
                case BOARD_ACTIONS.PLACE_OBJECT_ON_STAGE:
                    commit('PUSH_OBJECT', message.object);
                    break;
                case BOARD_ACTIONS.MOVE_TO:
                    commit('UPDATE_OBJECT', message.object);
                    break;
                case BOARD_ACTIONS.DESTROY:
                    commit('DELETE_OBJECT', message.object);
                    break;
                case BOARD_ACTIONS.SWITCH_FRAME:
                    commit('UPDATE_OBJECT', message.object);
                    break;
                case BOARD_ACTIONS.SPEAK:
                    commit('SET_OBJECT_SPEAK', message);
                    break;
                case BOARD_ACTIONS.SEND_TO_BACK:
                    commit('SEND_TO_BACK', message.object);
                    break;
                case BOARD_ACTIONS.BRING_TO_FRONT:
                    commit('BRING_TO_FRONT', message.object);
                    break;
                case BOARD_ACTIONS.BRING_TO_FRONT_OF:
                    commit('BRING_TO_FRONT_OF', message);
                    break;
                case BOARD_ACTIONS.TOGGLE_AUTOPLAY_FRAMES:
                    commit('UPDATE_OBJECT', message.object);
                    break;
                default:
                    break;
            }
        },
        setBackground(action, background) {
            background.at = +new Date()
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.CHANGE_BACKGROUND, background })
        },
        showChatBox(action, visible) {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.SET_CHAT_VISIBILITY, visible })
        },
        setBackdropColor(action, color) {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.SET_BACKDROP_COLOR, color })
        },
        drawCurtain(action, curtain) {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.DRAW_CURTAIN, curtain })
        },
        loadScenes() {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.LOAD_SCENES })
        },
        switchScene(action, scene) {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.SWITCH_SCENE, scene })
        },
        blankScene() {
            mqtt.sendMessage(TOPICS.BACKGROUND, { type: BACKGROUND_ACTIONS.BLANK_SCENE })
        },
        handleBackgroundMessage({ commit, dispatch }, { message }) {
            switch (message.type) {
                case BACKGROUND_ACTIONS.CHANGE_BACKGROUND:
                    commit('SET_BACKGROUND', message.background);
                    break;
                case BACKGROUND_ACTIONS.SET_CHAT_VISIBILITY:
                    commit('SET_CHAT_VISIBILITY', message.visible)
                    break;
                case BACKGROUND_ACTIONS.SET_BACKDROP_COLOR:
                    commit('SET_BACKDROP_COLOR', message.color)
                    break;
                case BACKGROUND_ACTIONS.DRAW_CURTAIN:
                    commit('SET_CURTAIN', message.curtain)
                    break;
                case BACKGROUND_ACTIONS.LOAD_SCENES:
                    dispatch('reloadScenes')
                    break;
                case BACKGROUND_ACTIONS.SWITCH_SCENE:
                    dispatch('replaceScene', message.scene)
                    break;
                case BACKGROUND_ACTIONS.BLANK_SCENE:
                    commit("REPLACE_SCENE", {
                        payload: JSON.stringify({
                            background: null,
                            board: { objects: [] },
                            audioPlayers: [],
                        }),
                    });
                    break;
                default:
                    break;
            }
        },
        updateAudioStatus(_, audio) {
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
        addDrawing({ commit, dispatch }, drawing) {
            drawing.type = 'drawing';
            commit('PUSH_DRAWING', drawing);
            return dispatch('placeObjectOnStage', drawing);
        },
        addStream({ commit, dispatch }, stream) {
            stream.type = 'stream';
            commit('PUSH_STREAM_TOOL', stream);
            dispatch('placeObjectOnStage', stream)
        },
        addText({ commit, dispatch }, text) {
            text.type = 'text';
            commit('PUSH_TEXT', text);
            dispatch('placeObjectOnStage', text)
        },
        handleReactionMessage({ commit }, { message }) {
            commit('PUSH_REACTION', message)
        },
        sendReaction(_, reaction) {
            mqtt.sendMessage(TOPICS.REACTION, reaction);
        },
        async loadStage({ commit, dispatch }, { url, recordId }) {
            commit('CLEAN_STAGE', true);
            commit('SET_PRELOADING_STATUS', true);
            const { stage, shapes, curtains } = await stageGraph.loadStage(url, recordId)
            if (stage) {
                commit('SET_MODEL', stage);
                commit('PUSH_SHAPES', shapes)
                commit('PUSH_CURTAINS', curtains)
                const { events } = stage
                if (recordId) {
                    commit('SET_REPLAY', {
                        timestamp: {
                            begin: events[0].mqttTimestamp,
                            current: events[0].mqttTimestamp,
                            end: events[events.length - 1].mqttTimestamp,
                        }
                    })
                } else {
                    events.forEach(event => dispatch('replayEvent', event));
                }
            } else {
                commit('SET_PRELOADING_STATUS', false);
            }
        },
        async reloadPermission({ state }) {
            const permission = await stageGraph.loadPermission(state.model.fileLocation)
            if (permission) {
                state.model.permission = permission
            }
        },
        async reloadScenes({ state }) {
            const scenes = await stageGraph.loadScenes(state.model.fileLocation)
            if (scenes) {
                state.model.scenes = scenes
            }
        },
        replaceScene({ state, commit, dispatch }, sceneId) {
            anime({
                targets: "#live-stage",
                filter: 'brightness(0)'
            });
            const scene = state.model.scenes.find(s => s.id == sceneId)
            if (scene) {
                commit('REPLACE_SCENE', scene)
            } else {
                setTimeout(() => dispatch('replaceScenes', sceneId), 1000) // If the scene is not loaded completely, retry after 1 second
            }
        },
        replayEvent({ dispatch }, { topic, payload }) {
            dispatch("handleMessage", {
                topic: unnamespaceTopic(topic),
                message: JSON.parse(payload),
            })
        },
        async replayRecord({ state, dispatch, commit }, timestamp) {
            await dispatch('pauseReplay');
            const current = timestamp ? Number(timestamp) : state.replay.timestamp.begin
            state.replay.timestamp.current = current
            commit('CLEAN_STAGE')
            state.replay.isReplaying = true
            const events = state.model.events
            const speed = state.replay.speed
            state.replay.interval = setInterval(() => {
                state.replay.timestamp.current += 10
                if (state.replay.timestamp.current > state.replay.timestamp.end) {
                    dispatch('pauseReplay');
                }
            }, 1000 / speed)
            events.forEach(event => {
                const timer = setTimeout(() => {
                    dispatch('replayEvent', event);
                }, (event.mqttTimestamp - current) * 100 / speed)
                state.replay.timers.push(timer)
            });
        },
        pauseReplay({ state }) {
            clearInterval(state.replay.interval)
            state.replay.interval = null
            state.replay.timers.forEach(timer => clearTimeout(timer))
            state.replay.timers = []
        },
        handleCounterMessage({ commit, state }, { message }) {
            commit('UPDATE_SESSIONS_COUNTER', message)
            if (message.id === state.session && message.avatarId) {
                commit('user/SET_AVATAR_ID', message.avatarId, { root: true });
            }
        },
        async joinStage({ rootGetters, state, rootState, commit }) {
            if (!state.session) {
                state.session = rootState.user.user?.id ?? uuidv4()
            }
            const id = state.session
            const isPlayer = rootGetters['auth/loggedIn'];
            const nickname = rootGetters['user/nickname'];
            const avatarId = rootGetters['user/avatarId'];
            commit('SET_ACTIVE_MOVABLE', avatarId)
            const at = +new Date();
            const payload = { id, isPlayer, nickname, at, avatarId }
            await mqtt.sendMessage(TOPICS.COUNTER, payload);
        },
        async leaveStage({ state, commit, dispatch }) {
            const id = state.session
            state.session = null
            commit('CLEAN_STAGE')
            await mqtt.sendMessage(TOPICS.COUNTER, { id, leaving: true });
            await dispatch('sendStatistics')
        },
        async sendStatistics({ state, getters }) {
            if (state.subscribeSuccess) {
                await mqtt.sendMessage(TOPICS.STATISTICS, { players: getters.players.length, audiences: getters.audiences.length });
            }
        },
        async getRunningStreams({ state, commit }) {
            state.loadingRunningStreams = true
            const streams = await nmsService.getStreams()
            commit('PUSH_RUNNING_STREAMS', streams)
            state.loadingRunningStreams = false
        },
        clearChat() {
            mqtt.sendMessage(TOPICS.CHAT, { clear: true })
        },
    },
};
