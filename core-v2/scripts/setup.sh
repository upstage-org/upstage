#!/bin/sh
formatted_date=$(date +"%d_%m_%Y")
echo "Formatted Date: $formatted_date"
mv src/global_config/config_formatted_date.py src/global_config/config_$formatted_date.py
export TIMESTAMP=$formatted_date