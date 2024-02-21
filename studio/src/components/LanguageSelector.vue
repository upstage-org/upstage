<template>
  <div class="locale-changer">
    <a-select
      v-model:value="$i18n.locale"
      @update:value="persistLocale"
      class="w-full"
    >
      <a-select-option
        v-for="locale in $i18n.availableLocales"
        :key="locale"
        :value="locale"
      >
        {{ flags[locale] ?? "🏳️‍🌈" }} {{ labels[locale] ?? locale }}
      </a-select-option>
    </a-select>
  </div>
</template>

<script setup>
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
