<script lang="ts" setup>
import { useMutation } from "@vue/apollo-composable";
import { ref } from "@vue/reactivity";
import configs from "config";
import gql from "graphql-tag";
import { getSharedAuth } from "utils/common";

const auth = ref<{ refresh_token: string; token: string }>();

const sharedState = getSharedAuth();
auth.value = sharedState;

const isDev = import.meta.env.DEV;

const { mutate } = useMutation<
  { authUser: { accessToken: string; refreshToken: string } },
  { username: string; password: string }
>(gql`
  mutation Login($username: String, $password: String) {
    authUser(username: $username, password: $password) {
      accessToken
      refreshToken
    }
  }
`);
const handleQuickLogin = async () => {
  const username = prompt("Username:", "nguyenhongphat0")?.trim();
  if (username) {
    const password = prompt("Password:");
    if (password) {
      const res = await mutate({
        username,
        password,
      });
      alert(JSON.stringify(res));
    }
  }
};
</script>

<template>
  <slot v-if="auth"></slot>
  <a-result
    v-else
    status="403"
    title="UpStage Player Required"
    sub-title="Sorry, you are not authorized to access this page."
  >
    <template #extra>
      <a :href="`${configs.UPSTAGE_URL}/backstage`">
        <a-button type="primary">{{ $t("login") }}</a-button>
      </a>
      <a-tooltip title="Quick login for developers">
        <a-button v-if="isDev" @click="handleQuickLogin">🔑</a-button>
      </a-tooltip>
    </template>
  </a-result>
</template>
