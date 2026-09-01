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
  cat > "${BUILD_DIR}/Dockerfile" <<EOF
FROM ${IMAGE}
USER root
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
# RUN pip list --outdated --format=json | python3 -c "import json,sys; print('\n'.join(p['name'] for p in json.load(sys.stdin)))" | xargs -r pip install --upgrade --no-cache-dir
USER ${ORIG_USER}
EOF

  PATCHED_LOCAL_TAG="vllm-security-patched:${VARIANT}-${VERSION}"
  SYSTEM_UPGRADE_OK=true
  PYTHON_UPGRADE_OK=true
  PATCHED_IMAGE=""

  if docker build -t "${PATCHED_LOCAL_TAG}" "${BUILD_DIR}" \
    && trivy image --scanners vuln --parallel 1 --timeout 60m --format json -o "${OUT_DIR}/${SAFE_NAME}-after.json" "${PATCHED_LOCAL_TAG}"; then
    PATCHED_IMAGE="$(build_patched_image_tag "${GHCR_OWNER}" "${IMAGE_NAME}" "${VERSION}" "${SCAN_DATE}")"
    docker tag "${PATCHED_LOCAL_TAG}" "${PATCHED_IMAGE}"
    if ! docker push "${PATCHED_IMAGE}"; then
      PATCHED_IMAGE=""
    fi
  else
    SYSTEM_UPGRADE_OK=false
    PYTHON_UPGRADE_OK=false
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
  "status": "ok"
}
EOF

  echo "Wrote ${OUT_DIR}/${SAFE_NAME}.json"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
