import { createI18n } from 'vue-i18n';
import de from './de';
import en from './en';

const messages = {
  en: en,
  de: de
}

const i18n = createI18n({
  locale: 'de',
  fallbackLocale: 'en',
  messages
})

export default i18n;