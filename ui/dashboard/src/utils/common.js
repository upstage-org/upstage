export const isJson = (d) => {
  try {
    JSON.parse(d);
  } catch (e) {
    return false;
  }
  return true;
};

export const getRandomColor = () => {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};
