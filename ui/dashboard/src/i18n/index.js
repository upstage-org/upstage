import { createI18n } from "vue-i18n";
import de from "./de";
import en from "./en";
import vn from "./vn";

const persistedLocale = localStorage.getItem("locale");

const i18n = createI18n({
  locale: persistedLocale ?? "de",
  fallbackLocale: "en",
  messages: { en, de, vn },
});

export default i18n;
