<script setup lang="ts">
import { useAsyncState } from "@vueuse/core";
import { Layout, message } from "ant-design-vue";
import { TransferItem } from "ant-design-vue/lib/transfer";
import RichTextEditor from "components/editor/RichTextEditor.vue";
import configs from "config";
import { enableExperimentalFragmentVariables } from "graphql-tag";
import { useLoading } from "hooks/mutations";
import { studioClient } from "services/graphql";
import { displayName, titleCase } from "utils/common";
import { reactive } from "vue";
import { computed } from "vue";
import { watch } from "vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const subject = ref("");

const INITIAL_BODY_CONTENT = `<h1>Title</h1><p>Dear UpStage Users,</p><p>Thank you and best regards,</p><p><img src="https://upstage.live/img/upstage.00bba63e.png" alt="@upstage-org">`;

const body = ref(INITIAL_BODY_CONTENT);

const receiverEmails = ref<string[]>([]);
const bccEmails = ref<string[]>([]);

const customRecipients = ref<string[]>([]);

const filterRole = ref<number | undefined>();

const addCustomRecipient = () => {
  const email = prompt("Enter email: ");
  if (email) {
    if (/^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$/.test(email)) {
      if (!receiverEmails.value.includes(email)) {
        receiverEmails.value = receiverEmails.value.concat(email);
      }
      if (
        !receivers.value.adminPlayers?.edges.some(
          (e) => e?.node?.email === email,
        )
      ) {
        customRecipients.value = customRecipients.value.concat(email);
      }
    } else {
      message.error("Invalid email address!");
    }
  }
};

const {
  state: receivers,
  isReady,
  execute,
} = useAsyncState(
  () =>
    studioClient.query({
      adminPlayers: {
        __args: {
          role: filterRole.value,
        },
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
  { adminPlayers: null },
  { resetOnExecute: false },
);

watch(filterRole, () => execute(0));

const dataSource = computed<TransferItem[]>(() => {
  return customRecipients.value
    .map<TransferItem>((email) => ({
      key: email,
      title: email,
    }))
    .concat(
      receivers.value.adminPlayers?.edges.map<TransferItem>((user, i) => ({
        key: user?.node?.email ?? `${i}`,
        title: user?.node
          ? `${displayName(user.node)} <${user.node.email}>`
          : "",
      })) ?? [],
    );
});

const reset = () => {
  receiverEmails.value = [];
  subject.value = "";
  body.value = INITIAL_BODY_CONTENT;
};

const { proceed, loading } = useLoading(
  async () => {
    if (!subject.value) {
      throw "Please provide a subject for your email";
    }
    if (!body.value) {
      throw "Please provide a body for your email";
    }
    if (!receiverEmails.value.length) {
      throw "Please select at least one recipient";
    }
    receiverEmails.value = receiverEmails.value.filter((email) =>
      receivers.value.adminPlayers?.edges.some(
        (edge) => edge?.node?.email === email,
      ),
    );
    await studioClient.mutation({
      sendEmail: {
        __args: {
          subject: subject.value,
          body: body.value,
          recipients: receiverEmails.value
            .filter((email) => !bccEmails.value.includes(email))
            .join(","),
          bcc: receiverEmails.value
            .filter((email) => bccEmails.value.includes(email))
            .join(","),
        },
        success: true,
      },
    });
    setTimeout(() => {
      reset();
    }, 0);
  },
  {
    loading: "Sending email...",
    success: () =>
      `Email has been successfully sent to ${receiverEmails.value
        .map((email) =>
          bccEmails.value.includes(email) ? `${email} (BCC)` : email,
        )
        .join(", ")}!`,
  },
);
</script>

<template>
  <Layout class="bg-white rounded-lg overflow-y-auto">
    <div
      class="bg-white shadow rounded-tl rounded-tr p-2 px-4 sticky top-0 z-50 mb-6 flex justify-between items-center"
    >
      <h3 class="mb-0">Email Notification</h3>
      <a-button type="primary" @click="proceed" :loading="loading">
        <send-outlined />
        Send
      </a-button>
    </div>
    <a-form-item
      :label-col="{ xl: { span: 4 }, xxl: { span: 3 } }"
      :colon="false"
    >
      <template #label>
        <a-space direction="vertical">
          {{ t("to") }}
          <a-select
            allow-clear
            placeholder="Filter by role"
            :options="
              Object.entries(configs.ROLES).map(([key, id]) => ({
                value: id,
                label: titleCase(key),
              }))
            "
            v-model:value="filterRole"
          />
          <a-button type="dashed" @click="addCustomRecipient">
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
          :data-source="dataSource"
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
                <a-tag v-if="!title?.includes('<')">Custom recipient</a-tag>
              </span>
              <a-switch
                size="small"
                :checked="bccEmails.includes(key as string)"
                @change="
                  (checked, e) => {
                    bccEmails = bccEmails
                      .filter((email) => email !== key)
                      .concat(checked ? (key as string) : []);
                    e.stopPropagation();
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
      :label-col="{ xl: { span: 4 }, xxl: { span: 3 } }"
      :colon="false"
    >
      <a-input v-model:value="subject" />
    </a-form-item>
    <a-form-item
      label="Body"
      :label-col="{ xl: { span: 4 }, xxl: { span: 3 } }"
      :colon="false"
    >
      <RichTextEditor v-model="body" @click="console.log(body)" />
    </a-form-item>
  </Layout>
</template>
