<template>
  <div class="locale-changer m-2">
    <Dropdown
      v-model="$i18n.locale"
      :data="$i18n.availableLocales"
      :renderLabel="
        (locale) => `${flags[locale] ?? '🏳️‍🌈'} ${labels[locale] ?? locale}`
      "
      @update:modelValue="persistLocale"
    >
      <template #selected="{ item }"
        >{{ flags[item] ?? "🏳️‍🌈" }}
        <span class="is-hidden-mobile">{{
          labels[item] ?? item
        }}</span></template
      >
    </Dropdown>
  </div>
</template>

<script setup>
import Dropdown from "./form/Dropdown.vue";
const flags = {
  en: "🇬🇧",
  de: "🇩🇪",
  vn: "🇻🇳",
  fr: "🇫🇷",
  se: "🇸🇪",
};

const labels = {
  en: "English",
  de: "Deutsch",
  vn: "Tiếng Việt",
  fr: "Français",
  se: "Svenska",
};
const persistLocale = (locale) => {
  localStorage.setItem("locale", locale);
};
</script>
