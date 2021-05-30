import { v4 as uuidv4 } from "uuid";
import config from '@/config';

export const getUniqueKey = () => {
    return uuidv4().replaceAll('-', '')
}

export const getSubsribeLink = (key) => {
    return `http://${config.RTMP.server}:${config.RTMP.subscribePort}/live/${key}/index.m3u8`
}

export const getPublishLink = (key) => {
    return `rtmp://${config.RTMP.server}:${config.RTMP.publishPort}/app/${key}`
}