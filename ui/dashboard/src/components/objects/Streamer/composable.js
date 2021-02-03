import { onMounted, ref, watch } from "vue";
import { cropImageFromCanvas } from "@/utils/canvas";

export const useShape = (video, object) => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const src = ref();

    const loop = () => {
        if (!video.value.paused && !video.value.ended) {
            ctx.drawImage(video.value, 0, 0);
            src.value = cropImageFromCanvas(canvas).src;
            setTimeout(loop, 1000 / 30); // drawing at 30fps
        }
    }

    onMounted(() => video.value.addEventListener('play', loop))

    watch(() => object.shape, () => {
        const { shape } = object;
        const r = Math.max(object.w, object.h) / 2;
        switch (shape) {
            case 'circle':
                ctx.save();
                ctx.beginPath();
                ctx.arc(r, r, r, 0, Math.PI * 2, true);
                ctx.clip();
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                break;

            default:
                break;
        }
    }, { immediate: true })

    return { src }
}