import { createI18n } from "vue-i18n";
import de from "./de";
import en from "./en";
import vn from "./vn";
import fr from "./fr";
import se from "./se";

const persistedLocale = localStorage.getItem("locale");

const i18n = createI18n({
  locale: persistedLocale ?? "en",
  fallbackLocale: "en",
  messages: { en, de, vn, fr, se },
});

export default i18n;
