import { createRouter, createWebHistory } from "vue-router";
import StagesManagement from "views/stages/index.vue";
import MediaManagement from "views/media/index.vue";
import AdminSection from "views/admin/index.vue";
import PlayerManagement from "views/admin/player-management/index.vue";
import EmailNotifications from "views/admin/email-notifications/index.vue";
import Configuration from "views/admin/configuration/index.vue";
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
      meta: {
        background: "#C7DCA7",
      },
      children: [
        { path: "", component: StagesManagement },
        {
          path: "new-stage",
          component: () =>
            import("views/stages/StageManagement/index.vue"),
          children: [
            {
              path: "", component: () =>
                import("views/stages/StageManagement/General.vue")
            }
          ],
        },
        {
          path: "stage-management/:id",
          component: () =>
            import("views/stages/StageManagement/index.vue"),
          props: (route) => ({ id: route.params.id }),
          children: [
            {
              path: "",
              name: "Stage Management",
              component: () =>
                import("views/stages/StageManagement/General.vue")
            },
            {
              name: "Stage Customisation",
              path: "customisation",
              component: () =>
                import("views/stages/StageManagement/Customisation.vue"),
            },
            {
              name: "Stage Media",
              path: "media",
              component: () =>
                import("views/stages/StageManagement/Media.vue"),
            },
            {
              name: "Archive",
              path: "archive",
              component: () =>
                import("views/stages/StageManagement/Archive.vue"),
            },
          ],
        },
      ],
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
        background: "#E6F2FF",
      },
      children: [
        { path: "player", component: PlayerManagement },
        { path: "configuration/:section?", component: Configuration },
        { path: "email-notification", component: EmailNotifications },
      ],
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
