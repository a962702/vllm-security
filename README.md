# vLLM Image Security Scanner

Automated daily security scanning of the official [vLLM](https://github.com/vllm-project/vllm)
Docker images. Each day this pipeline:

1. Finds the last 10 non-prerelease vLLM releases.
2. Scans every published image variant (`gpu`, `cpu`, `rocm`) with
   [Trivy](https://github.com/aquasecurity/trivy) — OS packages and Python
   packages.
3. Patches the image in two layers and rescans the result:
   - OS: `apt-get upgrade`.
   - Python (`scripts/gen_patch.py` → `scripts/patch/apply_python.py`): each
     package Trivy reports with a fixed version is upgraded to the smallest
     fixed version, one package at a time, with every other installed package
     pinned to its current version (so torch & co. never move). CVEs in
     vendored copies are fixed through the parent (setuptools → 80.10.2;
     pip is removed when the image has uv). Known exceptions — packages built
     from source (ROCm `lmcache`) and fixes past setuptools 81 (drops
     `pkg_resources`) — are skipped and reported. Standalone `uv`/`uvx`
     binaries with findings (bundled rustls, uv itself) are replaced with the
     current uv release; other fixable non-OS, non-Python binaries are
     reported as `unhandled_binaries`.
   - If the Python layer fails to build, or the patched image can no longer
     import `vllm` / `pkg_resources`, the OS-only image is published instead
     (`python_upgrade_ok: false`). What was changed is recorded in the image at
     `/usr/share/vllm-security/patch-result.json`.
4. Publishes the before/after vulnerability counts and pushes patched
   images to `ghcr.io/<owner>/vllm-security/<image-name>:<version>-<scan-date>`
   (e.g. `vllm-openai`, `vllm-openai-cpu`, `vllm-openai-rocm`; scan-date is a
   UTC `YYYYMMDD` stamp).

Full dashboard with historical trends: see the GitHub Pages site linked
below once the first scan has run. The dashboard lists every patched image
with a copyable `docker pull` command, lets you pick any of the last 7
scanned days and drill into the complete per-image vulnerability report
(not just counts), and builds a prompt you can paste into an LLM to draft an
impact assessment for your security team.

Patched images are best-effort security-metrics artifacts, not supported
vLLM builds — functional correctness is not guaranteed.

## Latest Scan Summary

<!-- scan-summary:start -->

_Last scanned: 2026-11-07T07:05:18Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 15/387/2881/829/0 | 15/370/2844/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261107 |
| nightly | cpu | 18/488/1700/1137/0 | 18/479/1691/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261107 |
| nightly | rocm | 19/493/2278/1196/0 | 19/480/2263/1188/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261107 |
| v0.32.0 | gpu | 18/396/2890/835/0 | 15/370/2844/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261107 |
| v0.32.0 | cpu | 21/526/2666/1177/0 | 18/479/1691/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261107 |
| v0.32.0 | rocm | 56/908/3392/1722/0 | 19/480/1029/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261107 |
| v0.31.0 | gpu | 31/553/3735/996/0 | 16/372/2850/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261107 |
| v0.31.0 | cpu | 26/558/2724/1211/0 | 18/481/1697/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261107 |
| v0.31.0 | rocm | 56/915/3419/1743/0 | 19/482/1035/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261107 |
| v0.30.0 | gpu | 36/623/3899/1075/0 | 16/374/2851/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261107 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261107 |
| v0.30.0 | rocm | 56/918/3467/1744/0 | 19/484/1036/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261107 |
| v0.29.0 | gpu | 37/631/4032/1074/0 | 16/374/2858/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261107 |
| v0.29.0 | cpu | 36/705/3510/1351/0 | 18/483/1700/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261107 |
| v0.29.0 | rocm | 57/926/3519/1743/0 | 19/484/1043/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261107 |
| v0.28.0 | gpu | 37/647/4203/1086/0 | 16/374/2858/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261107 |
| v0.28.0 | cpu | 36/705/3568/1356/0 | 18/483/1700/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261107 |
| v0.28.0 | rocm | 56/926/3549/1745/0 | 18/484/1042/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261107 |
| v0.27.1 | gpu | 38/724/3693/1444/0 | 19/483/1694/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261107 |
| v0.27.1 | cpu | 36/708/3581/1356/0 | 18/483/1702/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261107 |
| v0.27.1 | rocm | 56/927/3573/1754/0 | 18/484/1044/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261107 |
| v0.27.0 | gpu | 38/724/3693/1444/0 | 19/483/1694/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261107 |
| v0.27.0 | cpu | 36/708/3581/1356/0 | 18/483/1702/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261107 |
| v0.27.0 | rocm | 56/927/3573/1754/0 | 18/484/1044/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261107 |
| v0.26.0 | gpu | 39/730/3717/1446/0 | 19/483/1695/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261107 |
| v0.26.0 | cpu | 37/714/3624/1363/0 | 18/483/1703/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261107 |
| v0.26.0 | rocm | 55/923/3573/1753/0 | 18/484/1045/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261107 |
| v0.25.1 | gpu | 44/893/4021/1747/0 | 19/483/1702/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261107 |
| v0.25.1 | cpu | 42/878/3932/1664/0 | 18/483/1710/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261107 |
| v0.25.1 | rocm | 55/934/3647/1757/0 | 18/484/1052/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261107 |

<!-- scan-summary:end -->
