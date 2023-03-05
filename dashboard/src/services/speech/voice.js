export const voices = {
  ca: "Catalan",
  cs: "Czech",
  de: "German",
  el: "Greek",
  "en/en": "English",
  "en/en-n": "English, regional",
  "en/en-rp": "English, regional",
  "en/en-sc": "English, Scottish",
  "en/en-us": "English, US",
  "en/en-wm": "English, regional",
  eo: "Esperanto",
  es: "Spanish",
  "es-la": "Spanish, Latin America",
  fi: "Finnish",
  fr: "French",
  hu: "Hungarian",
  it: "Italian",
  kn: "Kannada",
  la: "Latin",
  lv: "Latvian",
  nl: "Dutch",
  pl: "Polish",
  pt: "Portuguese, Brazil",
  "pt-pt": "Portuguese, European",
  ro: "Romanian",
  sk: "Slovak",
  sv: "Swedish",
  tr: "Turkish",
  zh: "Mandarin Chinese (Pinyin)",
  "zh-yue": "Cantonese Chinese",
};

export const getVoiceList = () => {
  return Object.keys(voices).map((key) => ({
    id: key,
    name: voices[key],
  }));
};

export const getDefaultVoice = () => {
  return "en/en-us";
};

export const isValidVoice = (voice) => {
  return Object.keys(voices).includes(voice);
};

export const variants = {
  f1: "Female 1",
  f2: "Female 2",
  f3: "Female 3",
  f4: "Female 4",
  f5: "Female 5",
  m1: "Male 1",
  m2: "Male 2",
  m3: "Male 3",
  m4: "Male 4",
  m5: "Male 5",
  m6: "Male 6",
  m7: "Male 7",
  croak: "Croak",
  klatt: "Klatt",
  klatt2: "Klatt2",
  klatt3: "Klatt3",
  whisper: "Whisper (male)",
  whisperf: "Whisper (female)",
};

export const getVariantList = () => {
  return Object.keys(variants).map((key) => ({
    id: key,
    name: variants[key],
  }));
};

export const getDefaultVariant = () => {
  return "f1";
};
