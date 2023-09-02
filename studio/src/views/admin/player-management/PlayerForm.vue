<script lang="ts">
import { useI18n } from "vue-i18n";
import {
  Button,
  Form,
  Input,
  Modal,
  Switch,
  Tooltip,
  message,
} from "ant-design-vue";
import { h } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import { AdminPlayer } from "models/studio";
import { PropType } from "vue";
import { ref } from "vue";
import useForm from "ant-design-vue/lib/form/useForm";
import { reactive } from "vue";
import { toRaw } from "vue";
import { GraphQLError } from "graphql";

export default {
  props: {
    player: {
      type: Object as PropType<AdminPlayer>,
      required: true,
    },
    onSave: {
      type: Function as PropType<(player: AdminPlayer) => Promise<void>>,
      required: true,
    },
    saving: {
      type: Object as PropType<{ value: boolean }>,
      default: false,
    },
  },
  setup(props) {
    const { t } = useI18n();

    const visible = ref(false);

    const values = reactive({
      firstName: props.player.firstName,
      lastName: props.player.lastName,
      displayName: props.player.displayName,
      email: props.player.email,
      active: props.player.active,
    });
    const { validate } = useForm(values, {});

    return () =>
      h(
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
                loading: props.saving.value,
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
                        "onUpdate:value": (value: string) =>
                          (values.email = value),
                      }),
                    ],
                  ),
                  h(
                    Form.Item,
                    {
                      label: t("status"),
                    },
                    [
                      h(Switch, {
                        checked: values.active,
                        "onUpdate:checked": (value: boolean) =>
                          (values.active = value),
                      }),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ],
      );
  },
};
</script>
