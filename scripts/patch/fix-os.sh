#!/usr/bin/env bash
# Upgrade every OS package that has a newer version in the image's apt sources.
set -euxo pipefail
if ! command -v apt-get >/dev/null; then
  echo "no apt-get in image; skipping OS upgrade"
  exit 0
fi
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends
apt-get clean
rm -rf /var/lib/apt/lists/*
