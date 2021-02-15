<template>
  <div>
    View Scenes wireframes
    <a
      href="https://github.com/upstage-org/mobilise/issues/64#issuecomment-740554084"
      target="_blank"
      >here</a
    >
    <div>{{ result }}</div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const userList = computed(() => store.state.user.userList);
    const result = computed(() =>
      userList.value ? JSON.stringify(userList.value) : "Loading..."
    );
    store.dispatch("user/getUserList");

    return { result };
  },
};
</script>

<style>
</style>