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

_Last scanned: 2026-11-13T03:37:18Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/184/1223/460/0 | 5/177/1190/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261113 |
| nightly | cpu | 16/485/1691/1137/0 | 16/478/1689/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261113 |
| nightly | rocm | 19/492/2276/1197/0 | 17/479/2262/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261113 |
| v0.33.0 | gpu | 30/565/2474/1094/0 | 5/177/1190/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261113 |
| v0.33.0 | cpu | 18/488/1705/1144/0 | 16/478/1689/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261113 |
| v0.33.0 | rocm | 29/657/1686/1396/0 | 17/479/1021/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261113 |
| v0.32.0 | gpu | 33/570/2480/1094/0 | 5/177/1190/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261113 |
| v0.32.0 | cpu | 30/655/2358/1351/0 | 16/478/1689/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261113 |
| v0.32.0 | rocm | 81/1168/2668/2167/0 | 17/479/1026/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261113 |
| v0.31.0 | gpu | 56/864/2853/1582/0 | 6/179/1196/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261113 |
| v0.31.0 | cpu | 35/688/2417/1385/0 | 16/480/1695/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261113 |
| v0.31.0 | rocm | 81/1175/2695/2188/0 | 17/481/1032/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261113 |
| v0.30.0 | gpu | 61/935/3007/1669/0 | 6/181/1196/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261113 |
| v0.30.0 | cpu | 7/41/45/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261113 |
| v0.30.0 | rocm | 81/1178/2743/2189/0 | 17/483/1033/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261113 |
| v0.29.0 | gpu | 62/943/3140/1668/0 | 6/181/1203/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261113 |
| v0.29.0 | cpu | 58/960/2812/1771/0 | 16/482/1692/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261113 |
| v0.29.0 | rocm | 82/1186/2795/2188/0 | 17/483/1040/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261113 |
| v0.28.0 | gpu | 65/967/3263/1717/0 | 6/181/1203/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261113 |
| v0.28.0 | cpu | 58/960/2870/1776/0 | 16/482/1692/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261113 |
| v0.28.0 | rocm | 81/1186/2825/2190/0 | 16/483/1039/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261113 |
| v0.27.1 | gpu | 60/979/3001/1864/0 | 17/482/1692/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261113 |
| v0.27.1 | cpu | 58/963/2883/1776/0 | 16/482/1694/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261113 |
| v0.27.1 | rocm | 81/1187/2849/2199/0 | 16/483/1041/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261113 |
| v0.27.0 | gpu | 60/979/3001/1864/0 | 17/482/1692/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261113 |
| v0.27.0 | cpu | 58/963/2883/1776/0 | 16/482/1694/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261113 |
| v0.27.0 | rocm | 81/1187/2849/2199/0 | 16/483/1041/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261113 |
| v0.26.0 | gpu | 61/985/3025/1866/0 | 17/482/1693/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261113 |
| v0.26.0 | cpu | 59/969/2926/1783/0 | 16/482/1695/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261113 |
| v0.26.0 | rocm | 80/1183/2849/2198/0 | 16/483/1042/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261113 |
| v0.25.1 | gpu | 69/1153/3298/2190/0 | 17/482/1700/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261113 |
| v0.25.1 | cpu | 67/1138/3203/2107/0 | 16/482/1702/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261113 |
| v0.25.1 | rocm | 80/1194/2923/2202/0 | 16/483/1049/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261113 |

<!-- scan-summary:end -->
