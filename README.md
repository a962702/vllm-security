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

_Last scanned: 2026-11-22T07:53:21Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 3/96/1006/303/0 | 3/89/973/252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261122 |
| nightly | cpu | 17/448/1500/1063/0 | 17/445/1498/1061/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261122 |
| nightly | rocm | 17/458/2126/1107/0 | 17/445/2112/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261122 |
| v0.34.0 | gpu | 8/238/1231/574/0 | 3/89/983/253/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261122 |
| v0.34.0 | cpu | 19/519/1606/1219/0 | 17/445/1498/1061/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261122 |
| v0.34.0 | rocm | 22/532/2255/1264/0 | 18/446/2112/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261122 |
| v0.33.0 | gpu | 42/774/1912/1600/0 | 3/89/983/253/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261122 |
| v0.33.0 | cpu | 21/528/1638/1226/0 | 17/445/1498/1061/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261122 |
| v0.33.0 | rocm | 40/809/1313/1724/0 | 18/446/865/1092/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261122 |
| v0.32.0 | gpu | 45/779/1918/1600/0 | 3/89/983/253/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261122 |
| v0.32.0 | cpu | 41/807/1946/1694/0 | 17/445/1498/1061/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261122 |
| v0.32.0 | rocm | 92/1320/2280/2495/0 | 18/446/859/1090/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261122 |
| v0.31.0 | gpu | 68/1081/2293/2088/0 | 4/91/989/254/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261122 |
| v0.31.0 | cpu | 46/848/2007/1728/0 | 17/447/1504/1062/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261122 |
| v0.31.0 | rocm | 92/1335/2308/2516/0 | 18/448/865/1091/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261122 |
| v0.30.0 | gpu | 73/1152/2447/2175/0 | 4/93/989/253/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261122 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261122 |
| v0.30.0 | rocm | 92/1338/2356/2517/0 | 18/450/866/1092/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261122 |
| v0.29.0 | gpu | 74/1160/2580/2174/0 | 4/93/996/254/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261122 |
| v0.29.0 | cpu | 69/1120/2412/2109/0 | 17/449/1515/1057/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261122 |
| v0.29.0 | rocm | 93/1346/2408/2516/0 | 18/450/873/1093/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261122 |
| v0.28.0 | gpu | 77/1185/2703/2223/0 | 4/93/996/254/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261122 |
| v0.28.0 | cpu | 69/1121/2470/2114/0 | 17/449/1515/1057/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261122 |
| v0.28.0 | rocm | 92/1347/2438/2518/0 | 17/450/871/1093/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261122 |
| v0.27.1 | gpu | 71/1140/2617/2196/0 | 18/449/1529/1091/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261122 |
| v0.27.1 | cpu | 69/1124/2483/2114/0 | 17/449/1517/1057/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261122 |
| v0.27.1 | rocm | 92/1348/2471/2527/0 | 17/450/883/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261122 |
| v0.27.0 | gpu | 71/1140/2617/2196/0 | 18/449/1529/1091/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261122 |
| v0.27.0 | cpu | 69/1124/2483/2114/0 | 17/449/1517/1057/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261122 |
| v0.27.0 | rocm | 92/1348/2471/2527/0 | 17/450/883/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261122 |
| v0.26.0 | gpu | 72/1146/2641/2198/0 | 18/449/1530/1092/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261122 |
| v0.26.0 | cpu | 70/1130/2526/2121/0 | 17/449/1518/1058/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261122 |
| v0.26.0 | rocm | 91/1344/2471/2526/0 | 17/450/884/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261122 |

<!-- scan-summary:end -->
