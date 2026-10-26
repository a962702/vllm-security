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

os_dockerfile="$(write_os_dockerfile "vllm/vllm-openai:v0.32.0" "vllm")"
assert_eq "FROM vllm/vllm-openai:v0.32.0" "$(echo "${os_dockerfile}" | head -1)" \
  "write_os_dockerfile builds on the original image"
assert_eq "USER vllm" "$(echo "${os_dockerfile}" | tail -1)" \
  "write_os_dockerfile restores the original user"

py_dockerfile="$(write_python_dockerfile "vllm-security-os:gpu-v0.32.0" "root")"
assert_eq "FROM vllm-security-os:gpu-v0.32.0" "$(echo "${py_dockerfile}" | head -1)" \
  "write_python_dockerfile builds on the OS-patched image"
if echo "${py_dockerfile}" | grep -q "apply_python.py /tmp/vllm-security/plan.json ${PATCH_RESULT_PATH}"; then
  echo "PASS: write_python_dockerfile runs apply_python.py with the plan and result path"
else
  echo "FAIL: write_python_dockerfile does not run apply_python.py as expected"
  fail=1
fi

result_file="$(mktemp)"
cat > "${result_file}" <<'JSON'
{"packages": [{"name": "certifi", "status": "upgraded"}, {"name": "uv", "status": "upgraded"},
              {"name": "x", "status": "failed"}, {"name": "y", "status": "already"}],
 "failed": 1, "pip_removed": true, "skipped": [{"name": "lmcache", "reason": "r"}]}
JSON
assert_eq '{"upgraded": 2, "failed": 1, "pip_removed": true, "skipped": ["lmcache"]}' \
  "$(summarize_patch_result "${result_file}")" \
  "summarize_patch_result condenses the in-image result file"
rm -f "${result_file}"

exit ${fail}
