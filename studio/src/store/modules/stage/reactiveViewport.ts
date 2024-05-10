import store from "store";

export const getViewport = () => ({
  width: window.innerWidth,
  height: window.innerHeight,
});

window.addEventListener("resize", () => {
  const oldSize = store.getters["stage/stageSize"].width;
  store.commit("stage/UPDATE_VIEWPORT", getViewport());
  const newSize = store.getters["stage/stageSize"].width;
  store.commit("stage/RESCALE_OBJECTS", newSize / oldSize);
});
