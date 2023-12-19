<script lang="ts" setup>

const sample = {
  image: 'https://dev-app1.upstage.org.nz/V4.0/static/assets/avatar/b3c600921fac49c082770db23da06cef.png?t=1628499235',
  content: `<b>Hồng Phát</b> is requesting access to your media <b>Julius</b>: <em>"Hey Helen, can I borrow him for my upcoming stage? Thank you!"</em>`,
  at: new Date()
}

const notifications = Array(10).fill(sample)
</script>

<template>
  <a-popover title="Notifications" trigger="click">
    <template #content>
      <a-list class="w-96 overflow-auto" style="height: 75vh">
        <a-list-item v-for="notification in notifications" key="{notification.id}" class="px-4">
          <a-list-item-meta>
            <template #avatar>
              <a-avatar class="my-2" :src="notification.image" />
            </template>
            <template #title>
              <div class="text-sm whitespace-pre-wrap mb-2" v-html="notification.content"></div>
              <a-space>
                <a-button type="primary">Approve</a-button>
                <a-button danger>Deny</a-button>
              </a-space>
            </template>
            <template #description>
              <d-date :value="notification.at" />
            </template>
          </a-list-item-meta>
        </a-list-item>
      </a-list>
    </template>
    <a-badge :count="notifications.length" class="relative top-1">
      <a-button type="text">
        <NotificationFilled />
      </a-button>
    </a-badge>
  </a-popover>
</template>