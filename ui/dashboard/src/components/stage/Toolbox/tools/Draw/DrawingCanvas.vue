<template>
  <canvas
    ref="el"
    :width="config.width"
    :height="config.height"
    class="drawing"
  >
    Your browser does not support the HTML5 canvas tag.
  </canvas>
</template>

<script>
import { computed, onMounted, reactive, ref } from "vue";
import { useStore } from "vuex";
export default {
  setup: () => {
    const el = ref();
    const data = reactive({});
    const store = useStore();
    const config = computed(() => store.getters["stage/config"]);

    onMounted(() => {
      const { value: canvas } = el;
      var ctx = canvas.getContext("2d");

      const draw = () => {
        ctx.beginPath();
        ctx.moveTo(data.prevX, data.prevY);
        ctx.lineTo(data.currX, data.currY);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.closePath();
      };

      const findxy = (res, e) => {
        if (res == "down") {
          data.prevX = data.currX;
          data.prevY = data.currY;
          data.currX = e.clientX - canvas.offsetLeft;
          data.currY = e.clientY - canvas.offsetTop;

          data.flag = true;
          data.dot_flag = true;
          if (data.dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = "black";
            ctx.fillRect(data.currX, data.currY, 2, 2);
            ctx.closePath();
            data.dot_flag = false;
          }
        }
        if (res == "up" || res == "out") {
          data.flag = false;
        }
        if (res == "move") {
          if (data.flag) {
            data.prevX = data.currX;
            data.prevY = data.currY;
            data.currX = e.clientX - canvas.offsetLeft;
            data.currY = e.clientY - canvas.offsetTop;
            draw();
          }
        }
      };

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

      canvas.width = w;
      canvas.height = h;
      ctx.putImageData(cut, 0, 0);

      var image = canvas.toDataURL(); //open cropped image in a new window
      var win = window.open(image, "_blank");
      win.focus();
      store.dispatch("stage/addDrawing", {
        src: image,
        x: pix.x[0],
        y: pix.y[0],
        w,
        h,
      });
    };

    window.crop = cropImageFromCanvas;

    return { el, config, cropImageFromCanvas };
  },
};
</script>

<style lang="scss" scoped>
.drawing {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  width: 100vw;
  background-color: rgba($color: #30ac45, $alpha: 0.3);
}
</style>