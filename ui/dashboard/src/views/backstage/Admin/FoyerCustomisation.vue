<template>
  <div class="columns is-vcentered">
    <div class="column is-2">
      <b>Title</b>
    </div>
    <template v-if="edit == 'title'">
      <div class="column">
        <Field
          v-model="title"
          required
          required-message="You should not leave the foyer title blank!"
        />
      </div>
      <div class="column is-narrow">
        <button
          class="button is-primary"
          :class="{ 'is-loading': loading }"
          @click="save('Foyer title saved successfully!', 'FOYER_TITLE', title); edit = null"
        >Save</button>
      </div>
    </template>
    <template v-else>
      <div class="column">{{ title }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'title'">Edit</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column is-2">
      <b>Description</b>
    </div>
    <template v-if="edit == 'description'">
      <div class="column">
        <RichTextEditor v-model="description" />
      </div>
      <div class="column is-narrow">
        <button
          class="button is-primary"
          :class="{ 'is-loading': loading }"
          @click="save('Foyer description saved successfully!', 'FOYER_DESCRIPTION', description); edit = null"
        >Save</button>
      </div>
    </template>
    <template v-else>
      <div class="column pre-wrap" v-html="description"></div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'description'">Edit</button>
      </div>
    </template>
  </div>
  <div class="columns is-vcentered">
    <div class="column is-2">
      <span
        class="has-tooltip-right"
        data-tooltip="Syntax: <title> (<url>)
For example: Development (https://github.com/upstage-org/upstage/)
Put the navigation links line by line. Put > before the line to make it nested inside parent menu.
For example:
About
> FAQ (https://upstage.org.nz/?page_id=115)
> Contact (/contact)
"
      >
        <b>Menu</b>
        <i class="fas fa-info-circle ml-1"></i>
      </span>
    </div>
    <template v-if="edit == 'menu'">
      <div class="column">
        <textarea class="textarea" rows="8" v-model="menu" />
      </div>
      <div class="column is-narrow">
        <button
          class="button is-primary"
          :class="{ 'is-loading': loading }"
          @click="save('Foyer menu saved successfully!', 'FOYER_MENU', menu); edit = null"
        >Save</button>
      </div>
    </template>
    <template v-else>
      <div class="column pre-wrap">{{ menu }}</div>
      <div class="column is-narrow">
        <button class="button is-primary" @click="edit = 'menu'">Edit</button>
      </div>
    </template>
  </div>
</template>

<script>
import Field from "@/components/form/Field";
import { useStore } from "vuex";
import { ref, watchEffect } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { configGraph } from "@/services/graphql";
import RichTextEditor from "@/components/form/RichTextEditor.vue";

export default {
  components: { Field, RichTextEditor },
  setup: () => {
    const store = useStore();

    const title = ref('')
    const description = ref('')
    const menu = ref('')
    const edit = ref();

    watchEffect(() => {
      if (store.state.config.foyer) {
        title.value = store.state.config.foyer.title
        description.value = store.state.config.foyer.description
        menu.value = store.state.config.foyer.menu
      }
    });

    const { loading, save } = useMutation(configGraph.saveConfig);

    return { title, description, menu, edit, save, loading };
  },
};
</script>

<style scoped>
.pre-wrap {
  white-space: pre-wrap;
}
</style>
