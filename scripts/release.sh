#!/bin/bash

# 1. Build the wheel
uv build

# 2. Commit any source changes
git add .
git commit -m "Prepare release $1"

# 3. Tag the release
git tag $1

# 4. Push commits and tag
git push origin main
git push origin $1
