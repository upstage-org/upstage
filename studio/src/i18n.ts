import { createI18n } from "vue-i18n";
import de from "./i18n/de";
import en from "./i18n/en";
import vn from "./i18n/vn";
import es from "./i18n/es";
import fr from "./i18n/fr";
import pt from "./i18n/pt";
import se from "./i18n/se";

const persistedLocale = localStorage.getItem("locale");

const i18n = createI18n({
  locale: persistedLocale ?? "en",
  fallbackLocale: "en",
  messages: { en, de, vn, fr, se, pt, es },
  legacy: false,
});

export default i18n;
