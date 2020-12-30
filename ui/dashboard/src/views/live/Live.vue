<template>
  <section class="hero bg-cover is-primary is-fullheight">
    <Toolbox />
    <Chat />
  </section>
</template>

<script>
import Chat from "@/components/stage/Chat";
import Toolbox from "@/components/tools/Toolbox";
export default {
  components: { Chat, Toolbox },
};
</script>

<style>
</style>