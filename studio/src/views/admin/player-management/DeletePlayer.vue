<script lang="ts">
import { useI18n } from "vue-i18n";
import { Button, Popconfirm, message } from "ant-design-vue";
import { h } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import { AdminPlayer } from "models/studio";
import { PropType } from "vue";
import gql from "graphql-tag";
import { useMutation } from "@vue/apollo-composable";

export default {
  props: {
    player: {
      type: Object as PropType<AdminPlayer>,
      required: true,
    },
    onDone: {
      type: Function as PropType<(player: AdminPlayer) => Promise<void>>,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();

    const { mutate: deleteUser, loading: deleting } = useMutation<
      {
        deleteUser: { success: boolean };
      },
      { id: string }
    >(gql`
      mutation DeleteUser($id: ID!) {
        deleteUser(inbound: { id: $id }) {
          success
        }
      }
    `);

    return () =>
      h(
        Popconfirm,
        {
          title: t("delete_player_confirm"),
          okText: t("yes"),
          cancelText: t("no"),
          onConfirm: async () => {
            try {
              await deleteUser({ id: props.player.id });
              await props.onDone?.(props.player);
            } catch (error) {
              message.error(
                error instanceof Error ? error.message : (error as string),
              );
            }
          },
        },
        h(
          Button,
          { danger: true },
          {
            icon: () => h(DeleteOutlined),
          },
        ),
      );
  },
};
</script>