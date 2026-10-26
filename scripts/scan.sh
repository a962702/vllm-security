#!/usr/bin/env bash
set -euo pipefail

# Required env vars: IMAGE_REPO, VERSION, VARIANT, GHCR_OWNER, OUT_DIR, SCAN_DATE

derive_image_name() {
  local image_repo="$1"
  echo "${image_repo##*/}"
}

build_patched_image_tag() {
  local ghcr_owner="$1" image_name="$2" version="$3" scan_date="$4"
  echo "ghcr.io/${ghcr_owner}/vllm-security/${image_name}:${version}-${scan_date}"
}

now_iso() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

PATCH_RESULT_PATH=/usr/share/vllm-security/patch-result.json

# Layer 1: OS packages (apt-get upgrade).
write_os_dockerfile() {
  local base="$1" orig_user="$2"
  cat <<EOF
FROM ${base}
USER root
COPY fix-os.sh /tmp/vllm-security/fix-os.sh
RUN bash /tmp/vllm-security/fix-os.sh && rm -rf /tmp/vllm-security
USER ${orig_user}
EOF
}

# Layer 2: Python packages, per the plan from gen_patch.py. The result file stays
# in the image so every patched image records what was changed.
write_python_dockerfile() {
  local base="$1" orig_user="$2"
  cat <<EOF
FROM ${base}
USER root
COPY . /tmp/vllm-security
RUN python3 -I /tmp/vllm-security/apply_python.py /tmp/vllm-security/plan.json ${PATCH_RESULT_PATH} \\
 && rm -rf /tmp/vllm-security
USER ${orig_user}
EOF
}

# Every module the original image can import must still import after patching.
SMOKE_MODULES="vllm pkg_resources"

smoke_test() {
  local base="$1" patched="$2" module
  for module in ${SMOKE_MODULES}; do
    if ! docker run --rm --entrypoint python3 "${base}" -c "import ${module}" >/dev/null 2>&1; then
      echo "base image cannot import ${module}; not checked"
      continue
    fi
    if ! docker run --rm --entrypoint python3 "${patched}" -c "import ${module}"; then
      echo "patched image can no longer import ${module}"
      return 1
    fi
  done
}

# Condense apply_python.py's result file into the summary's python_patch field.
summarize_patch_result() {
  python3 -c '
import json, sys
r = json.load(open(sys.argv[1]))
print(json.dumps({
    "upgraded": sum(p["status"] == "upgraded" for p in r["packages"]),
    "failed": r["failed"],
    "pip_removed": r["pip_removed"],
    "skipped": [s["name"] for s in r["skipped"]],
}))' "$1"
}

write_failure_summary() {
  local status="$1"
  cat > "${OUT_DIR}/${SAFE_NAME}.json" <<EOF
{"version":"${VERSION}","variant":"${VARIANT}","image":"${IMAGE}","scanned_at":"$(now_iso)","before":null,"after":null,"system_upgrade_ok":null,"python_upgrade_ok":null,"patched_image":null,"status":"${status}"}
EOF
}

main() {
  IMAGE="${IMAGE_REPO}:${VERSION}"
  SAFE_NAME="scan-${VERSION}-${VARIANT}"
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  IMAGE_NAME="$(derive_image_name "${IMAGE_REPO}")"

  : "${SCAN_DATE:?SCAN_DATE is required}"

  mkdir -p "${OUT_DIR}"

  echo "Pulling ${IMAGE}"
  if ! docker pull "${IMAGE}"; then
    write_failure_summary "pull_failed"
    exit 0
  fi

  echo "Scanning ${IMAGE} (before)"
  if ! trivy image --scanners vuln --parallel 1 --timeout 60m --format json -o "${OUT_DIR}/${SAFE_NAME}-before.json" "${IMAGE}"; then
    write_failure_summary "scan_failed"
    exit 0
  fi

  ORIG_USER="$(docker inspect --format '{{.Config.User}}' "${IMAGE}")"
  ORIG_USER="${ORIG_USER:-root}"

  BUILD_DIR="$(mktemp -d)"
  cp -r "${SCRIPT_DIR}/patch/." "${BUILD_DIR}/"

  OS_LOCAL_TAG="vllm-security-os:${VARIANT}-${VERSION}"
  PATCHED_LOCAL_TAG="vllm-security-patched:${VARIANT}-${VERSION}"
  PATCH_RESULT_FILE="${OUT_DIR}/patch-${VERSION}-${VARIANT}.json"
  SYSTEM_UPGRADE_OK=false
  PYTHON_UPGRADE_OK=false
  PATCH_SUMMARY="null"
  PATCHED_IMAGE=""

  write_os_dockerfile "${IMAGE}" "${ORIG_USER}" > "${BUILD_DIR}/Dockerfile.os"
  if docker build -f "${BUILD_DIR}/Dockerfile.os" -t "${OS_LOCAL_TAG}" "${BUILD_DIR}"; then
    SYSTEM_UPGRADE_OK=true
  else
    docker tag "${IMAGE}" "${OS_LOCAL_TAG}"
  fi

  # A failed or broken Python layer falls back to the OS-only image.
  write_python_dockerfile "${OS_LOCAL_TAG}" "${ORIG_USER}" > "${BUILD_DIR}/Dockerfile.python"
  if python3 "${SCRIPT_DIR}/gen_patch.py" --report "${OUT_DIR}/${SAFE_NAME}-before.json" \
       --image "${IMAGE}" --out "${BUILD_DIR}/plan.json" \
    && docker build -f "${BUILD_DIR}/Dockerfile.python" -t "${PATCHED_LOCAL_TAG}" "${BUILD_DIR}" \
    && smoke_test "${IMAGE}" "${PATCHED_LOCAL_TAG}"; then
    docker run --rm --entrypoint cat "${PATCHED_LOCAL_TAG}" "${PATCH_RESULT_PATH}" > "${PATCH_RESULT_FILE}"
    PATCH_SUMMARY="$(summarize_patch_result "${PATCH_RESULT_FILE}")"
    if [ "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["failed"])' "${PATCH_RESULT_FILE}")" = "0" ]; then
      PYTHON_UPGRADE_OK=true
    fi
  else
    echo "Python patch failed; falling back to the OS-only image"
    docker tag "${OS_LOCAL_TAG}" "${PATCHED_LOCAL_TAG}"
  fi

  if trivy image --scanners vuln --parallel 1 --timeout 60m --format json -o "${OUT_DIR}/${SAFE_NAME}-after.json" "${PATCHED_LOCAL_TAG}"; then
    PATCHED_IMAGE="$(build_patched_image_tag "${GHCR_OWNER}" "${IMAGE_NAME}" "${VERSION}" "${SCAN_DATE}")"
    docker tag "${PATCHED_LOCAL_TAG}" "${PATCHED_IMAGE}"
    if ! docker push "${PATCHED_IMAGE}"; then
      PATCHED_IMAGE=""
    fi
  fi

  BEFORE_COUNTS="$(python3 "${SCRIPT_DIR}/aggregate.py" count-severity "${OUT_DIR}/${SAFE_NAME}-before.json")"
  if [ -f "${OUT_DIR}/${SAFE_NAME}-after.json" ]; then
    AFTER_COUNTS="$(python3 "${SCRIPT_DIR}/aggregate.py" count-severity "${OUT_DIR}/${SAFE_NAME}-after.json")"
  else
    AFTER_COUNTS="null"
  fi

  PATCHED_IMAGE_JSON="null"
  if [ -n "${PATCHED_IMAGE}" ]; then
    PATCHED_IMAGE_JSON="\"${PATCHED_IMAGE}\""
  fi

  cat > "${OUT_DIR}/${SAFE_NAME}.json" <<EOF
{
  "version": "${VERSION}",
  "variant": "${VARIANT}",
  "image": "${IMAGE}",
  "scanned_at": "$(now_iso)",
  "before": ${BEFORE_COUNTS},
  "after": ${AFTER_COUNTS},
  "system_upgrade_ok": ${SYSTEM_UPGRADE_OK},
  "python_upgrade_ok": ${PYTHON_UPGRADE_OK},
  "patched_image": ${PATCHED_IMAGE_JSON},
  "python_patch": ${PATCH_SUMMARY},
  "status": "ok"
}
EOF

  echo "Wrote ${OUT_DIR}/${SAFE_NAME}.json"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
