// @ts-nocheck
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { cropImageFromCanvas } from "utils/canvas";
import flvjs from "flv.js";

export const useShape = (video, object) => {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  const src = ref();

  const draw = () => {
    if (video.value) {
      ctx.drawImage(video.value, 0, 0, object.w, object.h);
      src.value = cropImageFromCanvas(canvas)?.src;
    }
  };

  const loop = () => {
    if (!video.value.paused && !video.value.ended) {
      draw();
      requestAnimationFrame(loop);
    }
  };

  onMounted(() => video.value.addEventListener("play", loop));

  const clipImage = (src) =>
    new Promise((resolve) => {
      const img = document.createElement("img");
      img.onload = function () {
        ctx.drawImage(img, 0, 0, object.w, object.h);
        ctx.globalCompositeOperation = "source-in";
        resolve();
      };
      img.onerror = () => {
        resolve();
      };
      img.src = src;
    });

  const resizeCanvas = () => {
    canvas.width = object.w;
    canvas.height = object.h;
  };
  watch(() => object.w, resizeCanvas);
  watch(() => object.h, resizeCanvas);

  watch(
    () => object.shape,
    async () => {
      const { shape } = object;
      const r = Math.min(object.w, object.h) / 2;
      canvas.width = object.w;
      canvas.height = object.h;
      if (video.value) {
        video.value.pause();
      }
      switch (shape) {
        case "circle":
          ctx.beginPath();
          ctx.arc(r, r, r, 0, Math.PI * 2, true);
          ctx.clip();
          break;

        case null:
          ctx.restore();
          break;

        default:
          await clipImage(shape);
      }
      if (video.value && object.isPlaying) {
        video.value.play();
      } else {
        draw();
      }
    },
    { immediate: true },
  );

  return { src };
};

export const useFlv = (video, src) => {
  const playable = ref(flvjs.isSupported());

  const initPlayer = () => {
    if (flvjs.isSupported()) {
      const flvPlayer = flvjs.createPlayer({
        type: "flv",
        url: src.value + "?" + new Date(), // Since firefox cannot play multiple video with the same url (I don't know why, seem like a bug). I hack the url so that firefox treat thems as multiple url
      });
      flvPlayer.attachMediaElement(video.value);
      flvPlayer.load();
      flvPlayer.on(flvjs.Events.ERROR, () => {
        playable.value = false;
      });
      video.value.addEventListener(
        "ended",
        () => {
          playable.value = false;
        },
        { once: true },
      );
    }
  };

  onMounted(initPlayer);
  watch(src, initPlayer);

  return { playable };
};

export const useCatchup = (video) => {
  const onProgress = () => {
    if (video.value.buffered.length) {
      var end = video.value.buffered.end(0);
      var delta = end - video.value.currentTime;
      if (delta > 3) {
        video.value.currentTime = end - 0.5;
      }
    }
  };
  onMounted(() => {
    video.value.addEventListener("progress", onProgress);
  });
  onBeforeUnmount(() => {
    video.value.removeEventListener("progress", onProgress);
  });
};
