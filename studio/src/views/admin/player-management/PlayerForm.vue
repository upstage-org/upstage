<script lang="ts">
import { useI18n } from "vue-i18n";
import {
  Button,
  Form,
  Input,
  Modal,
  Select,
  Switch,
  Textarea,
  Tooltip,
  message,
} from "ant-design-vue";
import { h, watch } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import { PropType } from "vue";
import { ref } from "vue";
import useForm from "ant-design-vue/lib/form/useForm";
import { reactive } from "vue";
import { toRaw } from "vue";
import { humanFileSize } from "utils/common";
import { User } from "models/studio";

export default {
  props: {
    player: {
      type: Object as PropType<User>,
      required: true,
    },
    onSave: {
      type: Function as PropType<(player: User) => Promise<void>>,
      required: true,
    },
    saving: Boolean,
    noUploadLimit: Boolean,
    noStatusToggle: Boolean,
    disabledIntroduction: Boolean,
  },
  setup(props, { slots }) {
    const { t } = useI18n();

    const visible = ref(false);

    const values = reactive({ ...props.player });

    const { validate, resetFields } = useForm(values, {});

    watch(
      () => props.player,
      (newValues) => resetFields(newValues),
    );

    watch(visible, (val) => {
      if (!val) {
        resetFields();
      }
    });

    const customLimit = ref("");

    return () => [
      h(
        Modal,
        {
          title: t("profile_title", { name: props.player.username }),
          visible: visible.value,
          onCancel: () => (visible.value = false),
          onOk: async () => {
            try {
              await validate();
              await props.onSave?.({
                ...props.player,
                ...toRaw(values),
              });
              visible.value = false;
            } catch (error) {
              message.error(
                error instanceof Error ? error.message : (error as string),
              );
            }
          },
          okButtonProps: {
            loading: props.saving,
          },
        },
        [
          h(
            Form,
            {
              layout: "horizontal",
              labelCol: { span: 6 },
              wrapperCol: { span: 18 },
            },
            [
              h(
                Form.Item,
                {
                  label: t("first_name"),
                },
                [
                  h(Input, {
                    value: values.firstName,
                    "onUpdate:value": (value: string) =>
                      (values.firstName = value),
                  }),
                ],
              ),
              h(
                Form.Item,
                {
                  label: t("last_name"),
                },
                [
                  h(Input, {
                    value: values.lastName,
                    "onUpdate:value": (value: string) =>
                      (values.lastName = value),
                  }),
                ],
              ),
              h(
                Form.Item,
                {
                  label: t("display_name"),
                  help: "In stage chat nickname",
                },
                [
                  h(Input, {
                    value: values.displayName,
                    "onUpdate:value": (value: string) =>
                      (values.displayName = value),
                  }),
                ],
              ),
              h(
                Form.Item,
                {
                  label: t("email"),
                },
                [
                  h(Input, {
                    value: values.email,
                    "onUpdate:value": (value: string) => (values.email = value),
                  }),
                ],
              ),
              h(
                Form.Item,
                {
                  label: t("introduction"),
                },
                [
                  h(Textarea, {
                    disabled: props.disabledIntroduction,
                    autoSize: true,
                    value: values.intro ?? "",
                    "onUpdate:value": (value: string) => (values.intro = value),
                  }),
                ],
              ),
              !props.noUploadLimit &&
                h(
                  Form.Item,
                  {
                    label: t("upload_limit"),
                  },
                  [
                    h(Select, {
                      class: "w-full",
                      dropdownMatchSelectWidth: false,
                      showSearch: true,
                      value: humanFileSize(
                        Number(values.uploadLimit),
                        false,
                        0,
                      ),
                      onSearch: (value) => {
                        customLimit.value = Math.min(
                          Number(value),
                          999,
                        ).toString();
                      },
                      options: ["2", "3", "5", "10", "100", "300"]
                        .map((value) => ({
                          value: `${value} MB`,
                        }))
                        .concat(
                          customLimit.value
                            ? [
                                {
                                  value: `${customLimit.value} MB`,
                                },
                              ]
                            : [],
                        ),
                      onChange: async (value) => {
                        const limit = Number(
                          (value as string).replace(" MB", ""),
                        );
                        const bytes = limit * 1024 * 1024;
                        values.uploadLimit = bytes;
                      },
                    }),
                  ],
                ),
              !props.noStatusToggle &&
                h(
                  Form.Item,
                  {
                    label: t("status"),
                  },
                  [
                    h(Switch, {
                      checked: values.active,
                      "onUpdate:checked": (value) =>
                        (values.active = value as boolean),
                    }),
                  ],
                ),
            ],
          ),
        ],
      ),
      slots.default
        ? slots.default({ onClick: () => (visible.value = true) })
        : h(
            Tooltip,
            {
              title: t("profile_title", { name: props.player.username }),
            },
            [
              h(
                Button,
                {
                  type: "primary",
                  onClick: () => (visible.value = true),
                },
                {
                  icon: () => h(EditOutlined),
                },
              ),
              ,
            ],
          ),
    ];
  },
};
</script>
