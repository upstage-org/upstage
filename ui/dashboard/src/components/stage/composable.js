import { onUnmounted, ref } from "vue";
import buildClient from "@/services/mqtt";
import { TOPICS } from "@/utils/constants";

export const useCounter = (stageUrl) => {
    const players = ref(0)
    const audiences = ref(0)
    const loading = ref(true)

    const mqtt = buildClient()
    const client = mqtt.connect();
    client.on("connect", () => {
        const topics = {
            [TOPICS.STATISTICS]: { qos: 2 },
        }
        mqtt.subscribe(topics, stageUrl).then(() => {
            loading.value = false
        })
    });
    client.on("error", (e) => {
        console.log(e)
    });
    mqtt.receiveMessage(({ message }) => {
        players.value = message.players
        audiences.value = message.audiences
    })

    onUnmounted(() => {
        mqtt.disconnect()
    })

    return [players, audiences, loading]
}