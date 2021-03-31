import config from '@/config';

export const isJson = (d) => {
  try {
    JSON.parse(d);
  } catch (e) {
    return false;
  }
  return true;
};

export const randomRange = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);

export const randomColor = () => {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

export const padZero = (str, len) => {
  len = len || 2;
  var zeros = new Array(len).join('0');
  return (zeros + str).slice(-len);
}

export const invertColor = (hex, bw) => {
  if (hex.indexOf('#') === 0) {
    hex = hex.slice(1);
  }
  // convert 3-digit hex to 6-digits.
  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  if (hex.length !== 6) {
    throw new Error('Invalid HEX color.');
  }
  var r = parseInt(hex.slice(0, 2), 16),
    g = parseInt(hex.slice(2, 4), 16),
    b = parseInt(hex.slice(4, 6), 16);
  if (bw) {
    // http://stackoverflow.com/a/3943023/112731
    return (r * 0.299 + g * 0.587 + b * 0.114) > 186
      ? '#000000'
      : '#FFFFFF';
  }
  // invert color components
  r = (255 - r).toString(16);
  g = (255 - g).toString(16);
  b = (255 - b).toString(16);
  // pad each with zeros and return
  return "#" + padZero(r) + padZero(g) + padZero(b);
}

export const randomMessageColor = () => {
  const bg = randomColor();
  const text = invertColor(bg, true)
  return { text, bg }
}

export function titleCase(str) {
  if (!str) {
    return ''
  }
  var splitStr = str.toLowerCase().replace(/_/g, ' ').split(' ');
  for (var i = 0; i < splitStr.length; i++) {
    splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
  }
  return splitStr.join(' ');
}

export function absolutePath(path) {
  return `${config.STATIC_ASSETS_ENDPOINT}${path}`
}

export function debounce(callback, delay) {
  let timeout;
  return () => {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(callback, delay)
  }
}