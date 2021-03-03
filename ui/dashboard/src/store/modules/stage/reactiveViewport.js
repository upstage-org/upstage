import store from "@/store";

export const getViewport = () => ({
    width: window.innerWidth,
    height: window.innerHeight
})

window.addEventListener("resize", () => {
    store.commit('stage/UPDATE_VIEWPORT', getViewport());
});