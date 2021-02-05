import { computed, onMounted, reactive, ref } from "vue";
import * as canvasUtil from '@/utils/canvas';

export const useDrawing = (color, size, mode) => {
    const el = ref(null);
    const data = reactive({
        history: []
    });

    const cropImageFromCanvas = () => {
        return canvasUtil.cropImageFromCanvas(el.value);
    };

    const eraseDot = (ctx) => {
        ctx.clearRect(data.currX, data.currY, size.value, size.value);
    }
    const drawDot = (ctx) => {
        ctx.beginPath();
        ctx.arc(data.currX, data.currY, size.value / 2, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.fillStyle = color.value;
        ctx.fill();
    };
    const draw = (ctx) => {
        ctx.beginPath();
        ctx.moveTo(data.prevX, data.prevY);
        ctx.lineTo(data.currX, data.currY);
        ctx.strokeStyle = color.value;
        ctx.lineWidth = size.value;
        ctx.stroke();
        ctx.closePath();
        drawDot(ctx);
    };
    const findxy = (res, e) => {
        const { value: canvas } = el;
        const ctx = canvas.getContext("2d");
        const { left, top } = canvas.getBoundingClientRect();
        if (res == "down") {
            data.prevX = data.currX;
            data.prevY = data.currY;
            data.currX = e.clientX - left;
            data.currY = e.clientY - top;

            data.flag = true;
            data.dot_flag = true;
            if (data.dot_flag) {
                if (mode.value === 'draw') {
                    drawDot(ctx);
                }
                if (mode.value === 'erase') {
                    eraseDot(ctx);
                }
            }
        }
        if (res == "up" || res == "out") {
            data.flag = false;
        }
        if (res == "up") {
            data.history.push(cropImageFromCanvas());
            data.dirty = true;
        }
        if (res == "move") {
            if (data.flag) {
                data.prevX = data.currX;
                data.prevY = data.currY;
                data.currX = e.clientX - left;
                data.currY = e.clientY - top;
                if (mode.value === 'draw') {
                    draw(ctx);
                }
                if (mode.value === 'erase') {
                    eraseDot(ctx);
                }
            }
        }
    };

    const attachEventLinsteners = () => {
        const { value: canvas } = el;
        if (canvas) {
            data.history = []
            canvas.addEventListener(
                "mousemove",
                (e) => {
                    findxy("move", e);
                },
                false
            );
            canvas.addEventListener(
                "mousedown",
                (e) => {
                    findxy("down", e);
                },
                false
            );
            canvas.addEventListener(
                "mouseup",
                (e) => {
                    findxy("up", e);
                },
                false
            );
            canvas.addEventListener(
                "mouseout",
                (e) => {
                    findxy("out", e);
                },
                false
            );
        }
    }

    onMounted(attachEventLinsteners)

    const clearCanvas = () => {
        const { value: canvas } = el;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        return ctx;
    }

    const undo = () => {
        const ctx = clearCanvas();
        let snapshot = data.history.pop();
        if (data.dirty) {
            snapshot = data.history.pop();
            data.dirty = false;
        }
        if (snapshot) {
            const image = document.createElement('img');
            image.onload = function () {
                ctx.drawImage(image, snapshot.x, snapshot.y);
            };
            image.src = snapshot.src;
        }
        return ctx;
    }

    const cursor = computed(() => {
        const canvas = document.createElement("canvas");
        canvas.width = size.value;
        canvas.height = size.value;
        const ctx = canvas.getContext("2d");
        if (mode.value === 'draw') {
            ctx.beginPath();
            const r = size.value / 2;
            ctx.arc(r, r, r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.fillStyle = color.value;
            ctx.fill();
            return `url(${canvas.toDataURL()}) ${r} ${r}, pointer`
        }
        if (mode.value === 'erase') {
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, size.value, size.value);
            ctx.strokeRect(0, 0, size.value, size.value);
        }
        return `url(${canvas.toDataURL()}), pointer`

    })

    return { el, cursor, cropImageFromCanvas, clearCanvas, undo }
}