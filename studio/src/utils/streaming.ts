import configs from "config";

export const getSubsribeLink = (key: string) => {
  return `${configs.STREAMING.subscribe}live/${key}.flv`;
};

export const getPublishLink = (key: string) => {
  return `${configs.STREAMING.publish}/${key}`;
};

export const getLarixLink = (key: string, sign: string, name: string) => {
  if (key.includes("?")) {
    key = key.substring(0, key.indexOf("?"));
  }
  const url = encodeURIComponent(getPublishLink(key) + `?sign=${sign}`);
  name = encodeURIComponent(name);
  return `larix://set/v1?conn[][url]=${url}&conn[][name]=${name}&conn[][overwrite]=on`;
};
