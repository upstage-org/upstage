<script lang="ts" setup>
import { PropType, computed } from "vue";
import { User } from "models/studio";

const { user } = defineProps({
  user: {
    type: Object as PropType<User>,
    default: 0,
  },
});

const text = computed(() => {
  if (user.displayName) {
    return `${user.displayName} (${user.username})`;
  }
  return user.username;
});
</script>

<template>
  {{ text }}
</template>
