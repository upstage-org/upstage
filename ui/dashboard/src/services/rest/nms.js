import configs from '@/config'
import axios from "axios";

export default {
    async getServerStatus() {
        const { subscribe, auth } = configs.STREAMING
        const url = `${subscribe}api/server`;
        const instance = axios.create({ auth });
        const { data } = await instance.get(url);
        return data;
    },
    async getStreams() {
        const { subscribe, auth } = configs.STREAMING
        const url = `${subscribe}api/streams`;
        const instance = axios.create({ auth });
        const { data } = await instance.get(url);
        const { live } = data
        const streams = []
        if (live) {
            Object.keys(live).forEach(key => {
                const { publisher } = live[key]
                if (publisher && publisher.video) {
                    const { width, height } = publisher.video
                    const stream = {
                        name: key,
                        type: 'stream',
                        isRTMP: true,
                        autoDetect: true,
                        url: key,
                    }
                    if (width > 0 && height > 0) {
                        stream.w = 100 * width / height;
                        stream.h = 100;
                        stream.ready = true;
                    }
                    streams.push(stream)
                }
            })
        }
        return streams;
    },
};
