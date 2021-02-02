import { ref, watch } from "vue";
import { cropImageFromCanvas } from "@/utils/canvas";

export const useShape = (video, shape) => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const src = ref();

    const loop = () => {
        if (!video.paused && !video.ended) {
            ctx.drawImage(video, 0, 0);
            src.value = cropImageFromCanvas(canvas).src;
            setTimeout(loop, 1000 / 30); // drawing at 30fps
        }
    }

    watch(shape, () => {
        let r = 0;
        switch (shape) {
            case 'circle':
                ctx.save();
                ctx.beginPath();
                r = canvas.height / 2;
                ctx.arc(r, r, r, 0, Math.PI * 2, true);
                ctx.clip();
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                break;

            default:
                break;
        }
    })

    video.addEventListener('play', loop);

    return { src }
}