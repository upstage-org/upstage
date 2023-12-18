<script lang="ts">
import { LayoutSider, Menu, MenuItem, Spin, SubMenu } from "ant-design-vue";
import { useRouter } from "vue-router";
import PlayerForm from "views/admin/player-management/PlayerForm.vue";
import { useUpdateProfile } from "hooks/auth";
import { h } from "vue";
import {
  PictureOutlined,
  CommentOutlined,
  ReadOutlined,
  UserOutlined,
  SettingOutlined,
} from "@ant-design/icons-vue";
import { computed } from "vue";
import configs from "config";

export default {
  setup(_, { slots }) {
    const router = useRouter();

    const { whoami, loading, save } = useUpdateProfile();

    const isAdmin = computed(
      () =>
        whoami.value &&
        [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
          whoami.value.role,
        ),
    );

    return () => [
      h(
        LayoutSider,
        {
          theme: "light",
          collapsible: true,
          collapsed: true,
          class: "select-none",
          width: 240,
        },
        [
          h(
            Spin,
            {
              spinning: loading.value,
            },
            h(
              Menu,
              {
                selectedKeys: [router.currentRoute.value.path],
                onSelect: (e) => router.push(e.key.toString()),
                mode: "inline",
                class: "upstage-menu",
              },
              [
                { key: "/media", icon: PictureOutlined, label: "Media" },
                { key: "/stages", icon: CommentOutlined, label: "Stages" },
                {
                  children: whoami.value
                    ? h(
                        PlayerForm,
                        {
                          player: whoami.value,
                          saving: loading.value,
                          onSave: save,
                          noUploadLimit: true,
                          noStatusToggle: true,
                        },
                        {
                          default: ({ onClick }: { onClick: () => void }) =>
                            h(
                              MenuItem,
                              {
                                onClick,
                              },
                              [h(UserOutlined), h("span", "Profile")],
                            ),
                        },
                      )
                    : h("span"),
                },
                ...(isAdmin.value
                  ? [
                      {
                        children: h(
                          SubMenu,
                          {
                            key: "/admin",
                            style: {
                              margin: 4,
                              background:
                                router.currentRoute.value.path.startsWith(
                                  "/admin",
                                )
                                  ? router.currentRoute.value.meta.background
                                  : undefined,
                            },
                          },
                          {
                            icon: () => h(SettingOutlined),
                            title: () => "Admin",
                            default: () => [
                              h(
                                MenuItem,
                                {
                                  key: "/admin/player",
                                },
                                "Player Management",
                              ),
                              h(
                                MenuItem,
                                {
                                  key: "/legacy/backstage/admin/foyer-customisation",
                                },
                                "Foyer Customisation",
                              ),
                              h(
                                MenuItem,
                                {
                                  key: "/legacy/backstage/admin/email-notification",
                                },
                                "Email Notification",
                              ),
                              h(
                                MenuItem,
                                {
                                  key: "/legacy/backstage/admin/system-configuration",
                                },
                                "System Configuration",
                              ),
                            ],
                          },
                        ),
                      },
                    ]
                  : []),
                {
                  key: "/legacy/https://docs.upstage.live/",
                  icon: ReadOutlined,
                  label: "Manual",
                },
              ].map((item) =>
                item.children
                  ? item.children
                  : h(
                      MenuItem,
                      {
                        key: item.key,
                        style: {
                          background:
                            item.key === router.currentRoute.value.path
                              ? router.currentRoute.value.meta.background
                              : undefined,
                        },
                      },
                      [h(item.icon), h("span", item.label)],
                    ),
              ),
            ),
          ),
        ],
      ),
      slots.default?.(),
    ];
  },
};
</script>

<style>
.ant-menu-submenu {
  margin: 4px;
}
.ant-menu-submenu-title {
  margin: 0 !important;
  width: 100% !important;
  padding-inline: calc(50% - 10px) !important;
}
</style>
