#!/bin/sh
# Builds assets/tailwind.css from the classes used in index.html (see tailwind.config.cjs).
cd "$(dirname "$0")/../.." && npx -y tailwindcss@3.4.17 -c tools/tailwind/tailwind.config.cjs -i tools/tailwind/input.css -o assets/tailwind.css --minify
