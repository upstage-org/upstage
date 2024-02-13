<script setup lang="ts">
import { useAsyncState } from "@vueuse/core";
import { Layout } from "ant-design-vue";
import { TransferItem } from "ant-design-vue/lib/transfer";
import RichTextEditor from "components/editor/RichTextEditor.vue";
import { studioClient } from "services/graphql";
import { displayName } from "utils/common";
import { watch } from "vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const content = ref(
  `<h1>Notification Title</h1><p>Dear UpStage Users,</p><p>Thank you and best regards,</p><p><img src="https://upstage.live/img/upstage.00bba63e.png" alt="@upstage-org">`
);

const receiverEmails = ref([]);
const bccEmails = ref<string[]>([]);

watch(bccEmails, console.log);

const { state: receivers, isReady } = useAsyncState(
  studioClient.query({
    adminPlayers: {
      edges: {
        node: {
          username: true,
          email: true,
          displayName: true,
          firstName: true,
          lastName: true,
        },
      },
    },
  }),
  { adminPlayers: null }
);
</script>

<template>
  <Layout class="bg-white rounded-lg overflow-y-auto">
    <div
      class="bg-white shadow rounded-tl rounded-tr p-2 px-4 sticky top-0 z-50 mb-6 flex justify-between items-center"
    >
      <h3 class="mb-0">Email Notification</h3>
      <a-button type="primary">
        <send-outlined />
        Send
      </a-button>
    </div>
    <a-form-item
      :label-col="{ span: 12, xl: { span: 4 }, xxl: { span: 3 } }"
      :colon="false"
    >
      <template #label>
        <a-space direction="vertical">
          {{ t("to") }}
          <a-select placeholder="Filter by role"></a-select>
          <a-button type="dashed">
            <plus-circle-outlined />
            Custom recipient
          </a-button>
        </a-space>
      </template>
      <a-spin :spinning="!isReady">
        <a-transfer
          :locale="{
            itemUnit: 'recipient',
            itemsUnit: 'recipients',
            notFoundContent: '',
            searchPlaceholder: 'Search by email or name',
          }"
          :list-style="{
            flex: '1',
            height: '300px',
          }"
          :titles="[' available', ' selected']"
          v-model:target-keys="receiverEmails"
          :data-source="(receivers.adminPlayers?.edges.map((user, i) => ({
              key: user?.node?.email ?? i,
              title: user?.node ? `${displayName(user.node)} <${user.node.email}>` : '',
            })) as TransferItem[])"
          show-search
          :filter-option="
            (keyword, option) =>
              option.title?.toLowerCase().includes(keyword.toLowerCase()) ??
              false
          "
        >
          <template #render="{ key, title }">
            <a-space class="flex justify-between">
              <span>
                {{ title }}
              </span>
              <a-switch
                size="small"
                :checked="bccEmails.includes(key as string)"
                @change="
                  (checked, e) => {
                    bccEmails = bccEmails
                      .filter((email) => email !== key)
                      .concat(checked ? key as string : []);
                      e.stopPropagation()
                  }
                "
              >
                <template #checkedChildren>
                  <span class="text-[8px] leading-none">BCC</span>
                </template>
                <template #unCheckedChildren>
                  <span class="text-[8px] leading-none">BCC</span>
                </template>
              </a-switch>
            </a-space>
          </template>
        </a-transfer>
      </a-spin>
    </a-form-item>
    <a-form-item
      label="Subject"
      :label-col="{ span: 12, xl: { span: 4 }, xxl: { span: 3 } }"
    >
      <a-input v-model="content" @click="console.log(content)" />
    </a-form-item>
    <a-form-item
      label="Body"
      :label-col="{ span: 12, xl: { span: 4 }, xxl: { span: 3 } }"
    >
      <RichTextEditor v-model="content" @click="console.log(content)" />
    </a-form-item>
  </Layout>
</template>
