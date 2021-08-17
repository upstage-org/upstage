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

export const getLarixLink = (key, sign, name) => {
    if (key.includes('?')) {
        key = key.substr(0, key.indexOf('?'))
    }
    const url = encodeURIComponent(getPublishLink(key) + `?sign=${sign}`)
    name = encodeURIComponent(name)
    return `larix://set/v1?conn[][url]=${url}&conn[][name]=${name}&conn[][overwrite]=on`
}