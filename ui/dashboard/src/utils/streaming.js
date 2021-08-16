import { v4 as uuidv4 } from "uuid";
import config from '@/config';

export const getUniqueKey = () => {
    return uuidv4().replaceAll('-', '')
}

export const getSubsribeLink = (key) => {
    return `${config.STREAMING.subscribe}live/${key}.flv`
}

export const getPublishLink = (key) => {
    return `${config.STREAMING.publish}/${key}`
}

export const getLarixLink = key => {
    return `larix://set/v1?conn[][url]=${key}`
}