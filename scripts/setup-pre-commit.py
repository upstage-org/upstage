import os

hook_file_path = ".git/hooks/pre-commit"

hook_contents = """#!/bin/sh

# Format Python codes
black .

# Format Front-end codes
npx prettier --write "./dashboard/*.{js,vue,json}" "./dashboard/src/**/*.{js,vue,json}"
npx prettier --write "./studio/*.{js,ts,vue,json}" "./studio/src/**/*.{js,ts,vue,json}"
"""

# Create the pre-commit hook file
with open(hook_file_path, "w") as f:
    f.write(hook_contents)

# Make the hook file executable
os.chmod(hook_file_path, 0o755)

print(f"Pre-commit hook file created at {hook_file_path} 🪝")
