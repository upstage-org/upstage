<script lang="ts">
import { LayoutSider, Menu, MenuItem, Spin, SubMenu } from "ant-design-vue";
import { useRouter } from "vue-router";
import PlayerForm from "views/admin/player-management/PlayerForm.vue";
import { useUpdateProfile } from "state/auth";
import { h, computed } from "vue";
import {
  PictureOutlined,
  CommentOutlined,
  ReadOutlined,
  UserOutlined,
  SettingOutlined,
} from "@ant-design/icons-vue";
import configs from "config";
import { useLoading } from "hooks/mutations";
import { settings } from "state/settings";

export default {
  async setup(_, { slots }) {
    const router = useRouter();

    const {
      whoami,
      updateProfile: save,
      loading: saving,
    } = await useUpdateProfile({
      loading: "Saving your profile...",
      success: () => "Your profile information saved successfully!",
    });

    const isAdmin = computed(
      () =>
        whoami.value &&
        [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
          whoami.value.role
        )
    );

    return () => [
      h(
        LayoutSider,
        {
          theme: "light",
          collapsed: true,
          class: "select-none",
          width: 240,
        },
        () => [
          h(
            Menu,
            {
              selectedKeys: [router.currentRoute.value.path],
              onSelect: (e) => router.push(e.key.toString()),
              mode: "inline",
              class: "upstage-menu",
            },
            () =>
              [
                { key: "/media", icon: PictureOutlined, label: "Media" },
                { key: "/stages", icon: CommentOutlined, label: "Stages" },
                {
                  children: whoami.value
                    ? h(
                        PlayerForm,
                        {
                          player: whoami.value,
                          saving: saving.value,
                          onSave: save as any,
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
                              () => [h(UserOutlined), h("span", "Profile")]
                            ),
                        }
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
                                  "/admin"
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
                                () => "Player Management"
                              ),
                              h(
                                MenuItem,
                                {
                                  key: "/admin/email-notification",
                                },
                                () => "Email Notification"
                              ),
                              h(
                                MenuItem,
                                {
                                  key: "/admin/configuration",
                                },
                                () => "Configuration"
                              ),
                            ],
                          }
                        ),
                      },
                    ]
                  : []),
                {
                  icon: ReadOutlined,
                  label: "Manual",
                  disabled: !settings.isReady.value,
                  onClick: () =>
                    open(
                      settings.state.value.system?.manual ??
                        "https://docs.upstage.live/",
                      "_blank"
                    ),
                },
              ].map((item) =>
                item.children
                  ? item.children
                  : h(
                      MenuItem,
                      {
                        key: item.key,
                        onClick: item.onClick,
                        disabled: item.disabled,
                        style: {
                          background:
                            item.key === router.currentRoute.value.path
                              ? router.currentRoute.value.meta.background
                              : undefined,
                        },
                      },
                      () => [h(item.icon), h("span", item.label)]
                    )
              )
          ),
        ]
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
state/auth
