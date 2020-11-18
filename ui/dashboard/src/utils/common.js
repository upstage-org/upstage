export const isJson = (d) => {
  try {
    JSON.parse(d);
  } catch (e) {
    return false;
  }
  return true;
};
