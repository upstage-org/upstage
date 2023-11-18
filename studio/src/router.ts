import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from "vue-router";
import StagesManagement from "views/stages/index.vue";
import MediaManagement from "views/media/index.vue";
import AdminSection from "views/admin/index.vue";
import PlayerManagement from "views/admin/player-management/index.vue";
import LegacyPage from "views/legacy.vue";

export const router = createRouter({
  history: createWebHistory("/studio/"),
  routes: [
    {
      path: "/",
      redirect: {
        path: "/stages",
      },
    },
    { path: "/stages", component: StagesManagement },
    { path: "/media", component: MediaManagement },
    {
      path: "/admin",
      component: AdminSection,
      children: [{ path: "player", component: PlayerManagement }],
    },
    {
      path: "/legacy/:path(.+)",
      component: LegacyPage,
    },
  ],
});
