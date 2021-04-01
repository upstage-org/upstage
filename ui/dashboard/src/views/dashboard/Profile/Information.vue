<template>
  <ProfileForm :profile="user" />
</template>

<script>
import { useStore } from "vuex";
import { computed } from "vue";
import ProfileForm from "@/components/ProfileForm";

export default {
  components: { ProfileForm },
  setup: () => {
    const store = useStore();
    const user = computed(() => store.state.user.user);

    return { user };
  },
};
</script>

<style>
</style>