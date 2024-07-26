#!/bin/bash
new_url=`grep VITE_API_ENDPOINT .env | awk -F= '{print $2}'`
cp ./staged_src/genql/studio/index.ts src/genql/studio/index.ts
cp ./staged_src/genql/config/index.ts src/genql/config/index.ts
sed -i "s@REPLACE_THIS_URL@${new_url}@g" src/genql/studio/index.ts
sed -i "s@REPLACE_THIS_URL@${new_url}@g" src/genql/config/index.ts
