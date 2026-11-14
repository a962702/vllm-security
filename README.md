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

_Last scanned: 2026-11-14T07:30:32Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/184/1232/460/0 | 5/177/1199/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261114 |
| nightly | cpu | 16/481/1702/1137/0 | 16/478/1695/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261114 |
| nightly | rocm | 19/492/2315/1197/0 | 17/478/2271/1190/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261114 |
| v0.33.0 | gpu | 30/610/2325/1232/0 | 5/177/1199/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261114 |
| v0.33.0 | cpu | 18/489/1735/1144/0 | 16/478/1695/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261114 |
| v0.33.0 | rocm | 29/691/1605/1484/0 | 17/479/1031/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261114 |
| v0.32.0 | gpu | 33/615/2331/1232/0 | 5/177/1199/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261114 |
| v0.32.0 | cpu | 30/689/2268/1439/0 | 16/478/1695/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261114 |
| v0.32.0 | rocm | 81/1202/2581/2255/0 | 17/479/1036/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261114 |
| v0.31.0 | gpu | 56/909/2704/1720/0 | 6/179/1205/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261114 |
| v0.31.0 | cpu | 35/722/2327/1473/0 | 16/480/1701/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261114 |
| v0.31.0 | rocm | 81/1209/2608/2276/0 | 17/481/1042/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261114 |
| v0.30.0 | gpu | 61/980/2858/1807/0 | 6/181/1205/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261114 |
| v0.30.0 | cpu | 7/42/46/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261114 |
| v0.30.0 | rocm | 81/1212/2656/2277/0 | 17/483/1043/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261114 |
| v0.29.0 | gpu | 62/988/2991/1806/0 | 6/181/1212/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261114 |
| v0.29.0 | cpu | 58/994/2718/1859/0 | 16/482/1694/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261114 |
| v0.29.0 | rocm | 82/1220/2708/2276/0 | 17/483/1050/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261114 |
| v0.28.0 | gpu | 65/1012/3114/1855/0 | 6/181/1212/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261114 |
| v0.28.0 | cpu | 58/994/2776/1864/0 | 16/482/1694/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261114 |
| v0.28.0 | rocm | 81/1220/2738/2278/0 | 16/483/1048/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261114 |
| v0.27.1 | gpu | 60/1013/2911/1952/0 | 17/482/1699/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261114 |
| v0.27.1 | cpu | 58/997/2789/1864/0 | 16/482/1696/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261114 |
| v0.27.1 | rocm | 81/1221/2762/2287/0 | 16/483/1050/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261114 |
| v0.27.0 | gpu | 60/1013/2911/1952/0 | 17/482/1699/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261114 |
| v0.27.0 | cpu | 58/997/2789/1864/0 | 16/482/1696/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261114 |
| v0.27.0 | rocm | 81/1221/2762/2287/0 | 16/483/1050/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261114 |
| v0.26.0 | gpu | 61/1019/2935/1954/0 | 17/482/1700/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261114 |
| v0.26.0 | cpu | 59/1003/2832/1871/0 | 16/482/1697/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261114 |
| v0.26.0 | rocm | 80/1217/2762/2286/0 | 16/483/1051/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261114 |
| v0.25.1 | gpu | 69/1187/3208/2278/0 | 17/482/1707/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261114 |
| v0.25.1 | cpu | 67/1172/3109/2195/0 | 16/482/1704/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261114 |
| v0.25.1 | rocm | 80/1228/2836/2290/0 | 16/483/1058/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261114 |

<!-- scan-summary:end -->
