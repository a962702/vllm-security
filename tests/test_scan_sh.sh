#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../scripts/scan.sh"

fail=0

assert_eq() {
  local expected="$1" actual="$2" desc="$3"
  if [ "${expected}" != "${actual}" ]; then
    echo "FAIL: ${desc}: expected '${expected}', got '${actual}'"
    fail=1
  else
    echo "PASS: ${desc}"
  fi
}

assert_eq "vllm-openai" "$(derive_image_name "vllm/vllm-openai")" \
  "derive_image_name strips namespace for gpu repo"
assert_eq "vllm-openai-cpu" "$(derive_image_name "vllm/vllm-openai-cpu")" \
  "derive_image_name strips namespace for cpu repo"
assert_eq "vllm-openai-rocm" "$(derive_image_name "vllm/vllm-openai-rocm")" \
  "derive_image_name strips namespace for rocm repo"

assert_eq \
  "ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260830" \
  "$(build_patched_image_tag "a962702" "vllm-openai-cpu" "v0.28.0" "20260830")" \
  "build_patched_image_tag composes ghcr path with image name, version, and scan date"

if grep -q -- "--pkg-types" "${SCRIPT_DIR}/../scripts/scan.sh"; then
  echo "FAIL: scan.sh must not restrict --pkg-types (Trivy should scan every package type)"
  fail=1
else
  echo "PASS: scan.sh does not restrict --pkg-types"
fi

exit ${fail}
