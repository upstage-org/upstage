<template>
  <div class="locale-changer my-2">
    <Dropdown v-model="$i18n.locale" :data="$i18n.availableLocales"
      :renderLabel="locale => `${flags[locale]} ${labels[locale]}`" />
  </div>
</template>

<script setup>
import Dropdown from './form/Dropdown.vue';
const flags = {
  en: '🇺🇸',
  de: '🇩🇪',
}
const labels = {
  en: 'English',
  de: 'Deutsch',
}
</script>