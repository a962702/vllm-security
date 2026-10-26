#!/usr/bin/env bash
# Remove every pip installation (pip vendors vulnerable urllib3/msgpack/setuptools).
# apt-owned pip is purged via apt so dpkg stays consistent; uv remains the package manager.
set -euo pipefail
if dpkg -s python3-pip >/dev/null 2>&1; then
    DEBIAN_FRONTEND=noninteractive apt-get purge -y python3-pip
fi
find / -xdev -type d \( -path '*-packages/pip' -o -path '*-packages/pip-*.dist-info' \) -prune -print 2>/dev/null |
while read -r d; do
    dpkg -S "$d" >/dev/null 2>&1 && { echo "skip apt-owned $d"; continue; }
    echo "remove $d"; rm -rf "$d"
done
# Drop now-broken pip entry points
find / -xdev -type f -regex '.*/bin/pip[0-9.]*' 2>/dev/null | while read -r f; do
    if grep -q 'pip._internal\|from pip' "$f" 2>/dev/null; then echo "remove $f"; rm -f "$f"; fi
done
# ensurepip bundled wheels also carry vendored copies
find / -xdev -path '*/ensurepip/_bundled/pip-*.whl' -print -delete 2>/dev/null || true
