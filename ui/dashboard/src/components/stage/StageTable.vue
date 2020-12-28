<template>
  <table class="table">
    <thead>
      <tr>
        <th><abbr title="Name (url)">Stage name</abbr></th>
        <th><abbr title="Duplicate/Manage stage">Actions</abbr></th>
        <th><abbr title="Chat log">Chat log</abbr></th>
        <th><abbr title="Screen recordings">Screen recordings</abbr></th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <th><abbr title="Name (url)">Stage name</abbr></th>
        <th><abbr title="Duplicate/Manage stage">Actions</abbr></th>
        <th><abbr title="Chat log">Chat log</abbr></th>
        <th><abbr title="Screen recordings">Screen recordings</abbr></th>
      </tr>
    </tfoot>
    <tbody>
      <tr v-for="stage in stages" :key="stage">
        <td>
          <router-link to="/live" class="has-text-primary has-text-weight-bold">
            {{ stage.name }}
          </router-link>
        </td>
        <td class="has-text-centered">
          <Modal>
            <template #trigger>
              <i class="fas fa-lg fa-cog" />
            </template>
            <template #header>Stage Detail</template>
            <template #content><Detail :name="stage.name" /></template>
            <template #footer><DuplicateButton /></template>
          </Modal>
        </td>
        <td class="has-text-centered">
          <i class="fas fa-lg fa-comments" />
        </td>
        <td class="has-text-centered">
          <i class="fas fa-lg fa-video" />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import Modal from "../Modal";
import DuplicateButton from "./DuplicateButton";
import Detail from "./Detail";

export default {
  components: { Modal, DuplicateButton, Detail },
  setup: () => {
    const stages = [
      {
        name: "Making Absence Present",
      },
      {
        name: "Waiting for Brexit",
      },
      {
        name: "Pandemic Party",
      },
    ];

    return { stages };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>