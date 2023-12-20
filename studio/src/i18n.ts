import { createI18n } from "vue-i18n";
import de from "../../dashboard/src/i18n/de";
import en from "../../dashboard/src/i18n/en";
import vn from "../../dashboard/src/i18n/vn";

const persistedLocale = localStorage.getItem("locale");

const i18n = createI18n({
  locale: persistedLocale ?? "en",
  fallbackLocale: "en",
  messages: { en, de, vn },
  legacy: false,
});

export default i18n;
