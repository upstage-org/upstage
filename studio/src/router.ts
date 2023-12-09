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
    {
      path: "/stages",
      component: StagesManagement,
      meta: {
        background: "#C7DCA7",
      },
    },
    {
      path: "/media",
      component: MediaManagement,
      meta: {
        background: "#FFEBD8",
      },
    },
    {
      path: "/admin",
      component: AdminSection,
      meta: {
        background: "#FFC5C5",
      },
      children: [{ path: "player", component: PlayerManagement }],
    },
    {
      path: "/legacy/:path(.+)",
      component: LegacyPage,
      meta: {
        background: "#E5E6E6",
      },
    },
  ],
});
