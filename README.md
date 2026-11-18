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

_Last scanned: 2026-11-18T08:23:27Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/192/1273/480/0 | 5/185/1240/429/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261118 |
| nightly | cpu | 16/491/1672/1173/0 | 16/488/1664/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261118 |
| nightly | rocm | 19/502/2296/1237/0 | 17/488/2252/1230/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261118 |
| v0.34.0 | gpu | 5/202/1277/504/0 | 5/185/1240/429/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261118 |
| v0.34.0 | cpu | 16/491/1672/1173/0 | 16/488/1664/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261118 |
| v0.34.0 | rocm | 19/503/2296/1237/0 | 17/489/2252/1230/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261118 |
| v0.33.0 | gpu | 39/736/1961/1528/0 | 5/185/1240/429/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261118 |
| v0.33.0 | cpu | 18/499/1705/1180/0 | 16/488/1664/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261118 |
| v0.33.0 | rocm | 37/779/1358/1697/0 | 17/489/1009/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261118 |
| v0.32.0 | gpu | 42/741/1967/1528/0 | 5/185/1240/429/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261118 |
| v0.32.0 | cpu | 38/777/2013/1648/0 | 16/488/1664/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261118 |
| v0.32.0 | rocm | 89/1290/2324/2468/0 | 17/489/1003/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261118 |
| v0.31.0 | gpu | 65/1043/2341/2016/0 | 6/187/1246/430/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261118 |
| v0.31.0 | cpu | 43/818/2073/1682/0 | 16/490/1670/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261118 |
| v0.31.0 | rocm | 89/1305/2352/2489/0 | 17/491/1009/1220/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261118 |
| v0.30.0 | gpu | 70/1114/2495/2103/0 | 6/189/1246/429/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261118 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261118 |
| v0.30.0 | rocm | 89/1308/2400/2490/0 | 17/493/1010/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261118 |
| v0.29.0 | gpu | 71/1122/2628/2102/0 | 6/189/1253/430/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261118 |
| v0.29.0 | cpu | 66/1090/2479/2066/0 | 16/492/1679/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261118 |
| v0.29.0 | rocm | 90/1316/2452/2489/0 | 17/493/1017/1222/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261118 |
| v0.28.0 | gpu | 74/1146/2751/2151/0 | 6/189/1253/430/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261118 |
| v0.28.0 | cpu | 66/1090/2537/2071/0 | 16/492/1679/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261118 |
| v0.28.0 | rocm | 89/1316/2482/2491/0 | 16/493/1015/1222/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261118 |
| v0.27.1 | gpu | 68/1109/2667/2166/0 | 17/492/1679/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261118 |
| v0.27.1 | cpu | 66/1093/2550/2071/0 | 16/492/1681/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261118 |
| v0.27.1 | rocm | 89/1317/2515/2500/0 | 16/493/1027/1232/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261118 |
| v0.27.0 | gpu | 68/1109/2667/2166/0 | 17/492/1679/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261118 |
| v0.27.0 | cpu | 66/1093/2550/2071/0 | 16/492/1681/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261118 |
| v0.27.0 | rocm | 89/1317/2515/2500/0 | 16/493/1027/1232/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261118 |
| v0.26.0 | gpu | 69/1115/2691/2168/0 | 17/492/1680/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261118 |
| v0.26.0 | cpu | 67/1099/2593/2078/0 | 16/492/1682/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261118 |
| v0.26.0 | rocm | 88/1313/2515/2499/0 | 16/493/1028/1232/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261118 |

<!-- scan-summary:end -->
