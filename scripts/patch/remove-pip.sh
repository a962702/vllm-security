#!/usr/bin/env bash
# Remove every pip installation (pip vendors vulnerable urllib3/msgpack/setuptools).
# uv remains the package manager.
# apt-owned pip is purged via apt so dpkg stays consistent -- but only when
# nothing else goes with it: on ROCm images rocm-dev and amd-smi-lib depend on
# python3-pip, and amd-smi-lib's libamd_smi is what vllm uses to find the GPUs.
# In that case apt's pip is kept and reported ("KEPT: ...").
set -euo pipefail
if dpkg -s python3-pip >/dev/null 2>&1; then
    also_removed="$(apt-get -s purge python3-pip | awk '/^Purg|^Remv/ && $2 != "python3-pip" {print $2}' | xargs)"
    if [ -z "${also_removed}" ]; then
        DEBIAN_FRONTEND=noninteractive apt-get purge -y python3-pip
    else
        echo "KEPT: apt-owned python3-pip, purging it would also remove: ${also_removed}"
    fi
fi
find / -xdev -type d \( -path '*-packages/pip' -o -path '*-packages/pip-*.dist-info' \) -prune -print 2>/dev/null |
while read -r d; do
    dpkg -S "$d" >/dev/null 2>&1 && { echo "skip apt-owned $d"; continue; }
    echo "remove $d"; rm -rf "$d"
done
# Drop now-broken pip entry points (apt-owned ones stay with their package)
find / -xdev -type f -regex '.*/bin/pip[0-9.]*' 2>/dev/null | while read -r f; do
    dpkg -S "$f" >/dev/null 2>&1 && continue
    if grep -q 'pip._internal\|from pip' "$f" 2>/dev/null; then echo "remove $f"; rm -f "$f"; fi
done
# ensurepip bundled wheels also carry vendored copies (apt-owned ones stay
# with their package, e.g. deadsnakes' python3.12-venv)
find / -xdev -path '*/ensurepip/_bundled/pip-*.whl' 2>/dev/null | while read -r f; do
    dpkg -S "$f" >/dev/null 2>&1 && { echo "skip apt-owned $f"; continue; }
    echo "remove $f"; rm -f "$f"
done
