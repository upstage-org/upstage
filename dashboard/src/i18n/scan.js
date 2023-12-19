const fs = require("fs");

const scanFolder = (path) => {
  const files = fs.readdirSync(path);
  for (const file of files) {
    if (fs.statSync(path + "/" + file).isDirectory()) {
      scanFolder(path + "/" + file);
    } else {
      processFile(path + "/" + file);
    }
  }
};

const processFile = (path) => {
  const filename = path.substring(path.lastIndexOf("/") + 1);
  const [_, extension] = filename.split(".");
  if (extension === "vue") {
    const regex = />[a-zA-Z0-9 ]+</g;
    const file = fs.readFileSync(path, "utf8");
    let found = false;
    const newContent = file.replace(regex, (match) => {
      if (!found) {
        console.log(`🔎 Found: ${path}`);
        found = true;
        fileChanged++;
      }
      const word = match.substring(1, match.length - 1).trim();
      const key = word.toLowerCase().replace(/ /g, "_");
      map[key] = word;
      const toReplace = `>{{ $t("${key}") }}<`;
      console.log(`✅ Replacing "${word}" with "${`{{ $t("${key}") }}`}"`);
      lineChanged++;
      return toReplace;
    });
    fs.writeFileSync(path, newContent);
  }
};

let fileChanged = 0;
let lineChanged = 0;
const map = {};
scanFolder("./src");
console.log(`📄 ${fileChanged} files changed`);
console.log(`📝 ${lineChanged} lines changed`);
console.log(`📦 Results:`);
console.log(map);
