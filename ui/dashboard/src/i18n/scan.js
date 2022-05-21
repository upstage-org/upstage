const fs = require('fs');

const scanFolder = (path) => {
  const files = fs.readdirSync(path);
  for (const file of files) {
    if (fs.statSync(path + '/' + file).isDirectory()) {
      scanFolder(path + '/' + file);
    } else {
      processFile(path + '/' + file);
    }
  }
}

const processFile = (path) => {
  const filename = path.substring(path.lastIndexOf('/') + 1);
  const [name, extension] = filename.split('.');
  if (extension === 'vue') {
    const regex = />[a-zA-Z0-9]+</g;
    const file = fs.readFileSync(path, 'utf8');
    const newContent = file.replace(regex, (match) => {
      const word = match.substring(1, match.length - 1).toLowerCase().replace(' ', '_');
      const toReplace = `>{{ $t("${word}") }}>`;
      return toReplace;
    });
    console.log(newContent);
  }
}

scanFolder('./src')