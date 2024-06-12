import { createI18n } from "vue-i18n";
import de from "./de";
import en from "./en";
import es from "./es";
import fr from "./fr";
import pt from "./pt";
import se from "./se";
import vn from "./vn";

const persistedLocale = localStorage.getItem("locale");

const i18n = createI18n({
  locale: persistedLocale ?? "en",
  fallbackLocale: "en",
  messages: { de, en, es, fr, pt, se, vn },
});

export default i18n;
