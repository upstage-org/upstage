import { computed, onMounted, reactive, ref } from "vue";

export const useDrawing = (color, size, mode) => {
    const el = ref();
    const data = reactive({
        history: []
    });

    const cropImageFromCanvas = () => {
        const { value: canvas } = el;

        var ctx = canvas.getContext("2d");
        var w = canvas.width,
            h = canvas.height,
            pix = { x: [], y: [] },
            imageData = ctx.getImageData(0, 0, canvas.width, canvas.height),
            x,
            y,
            index;

        for (y = 0; y < h; y++) {
            for (x = 0; x < w; x++) {
                index = (y * w + x) * 4;
                if (imageData.data[index + 3] > 0) {
                    pix.x.push(x);
                    pix.y.push(y);
                }
            }
        }
        pix.x.sort(function (a, b) {
            return a - b;
        });
        pix.y.sort(function (a, b) {
            return a - b;
        });
        var n = pix.x.length - 1;

        w = 1 + pix.x[n] - pix.x[0];
        h = 1 + pix.y[n] - pix.y[0];
        var cut = ctx.getImageData(pix.x[0], pix.y[0], w, h);

        const tmpCanvas = document.createElement('canvas');
        tmpCanvas.width = w;
        tmpCanvas.height = h;
        tmpCanvas.getContext('2d').putImageData(cut, 0, 0);

        const image = tmpCanvas.toDataURL();
        return {
            src: image,
            x: pix.x[0],
            y: pix.y[0],
            w,
            h,
        };
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

    onMounted(() => {
        const { value: canvas } = el;

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
    });

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
            console.log(size.value / 2)
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