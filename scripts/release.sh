#!/bin/bash

# Extract version from pyproject.toml
VERSION=$(grep -Po '(?<=^version = ")[^"]+' pyproject.toml)

echo "Releasing version $VERSION"

# 1️⃣ Build wheel
uv build

# 2️⃣ Commit source changes
git add .
git commit -m "Prepare release $VERSION"

# 3️⃣ Tag release
git tag v$VERSION

# 4️⃣ Push commit and tag
git push origin main
git push origin v$VERSION

echo "Release $VERSION ready! Upload wheel to GitHub release."
