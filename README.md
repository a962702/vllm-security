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

_Last scanned: 2026-11-24T10:50:08Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 10/134/1243/362/0 | 10/127/1210/311/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261124 |
| nightly | cpu | 23/478/1688/1108/0 | 23/475/1686/1106/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261124 |
| nightly | rocm | 23/488/2318/1152/0 | 23/475/2300/1146/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261124 |
| v0.34.0 | gpu | 15/276/1472/633/0 | 10/127/1220/312/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261124 |
| v0.34.0 | cpu | 25/549/1798/1264/0 | 23/475/1686/1106/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261124 |
| v0.34.0 | rocm | 28/562/2447/1309/0 | 24/476/2300/1146/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261124 |
| v0.33.0 | gpu | 49/812/2153/1659/0 | 10/127/1220/312/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261124 |
| v0.33.0 | cpu | 27/558/1830/1271/0 | 23/475/1686/1106/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261124 |
| v0.33.0 | rocm | 46/839/1505/1769/0 | 24/476/1053/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261124 |
| v0.32.0 | gpu | 52/817/2159/1659/0 | 10/127/1220/312/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261124 |
| v0.32.0 | cpu | 47/837/2138/1739/0 | 23/475/1686/1106/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261124 |
| v0.32.0 | rocm | 98/1350/2472/2540/0 | 24/476/1047/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261124 |
| v0.31.0 | gpu | 75/1119/2534/2147/0 | 11/129/1226/313/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261124 |
| v0.31.0 | cpu | 52/878/2199/1773/0 | 23/477/1692/1107/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261124 |
| v0.31.0 | rocm | 98/1365/2500/2561/0 | 24/478/1053/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261124 |
| v0.30.0 | gpu | 80/1190/2688/2234/0 | 11/131/1226/312/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261124 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261124 |
| v0.30.0 | rocm | 98/1368/2548/2562/0 | 24/480/1054/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261124 |
| v0.29.0 | gpu | 81/1198/2821/2233/0 | 11/131/1233/313/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261124 |
| v0.29.0 | cpu | 75/1150/2602/2154/0 | 23/479/1705/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261124 |
| v0.29.0 | rocm | 99/1376/2600/2561/0 | 24/480/1061/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261124 |
| v0.28.0 | gpu | 84/1223/2944/2282/0 | 11/131/1233/313/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261124 |
| v0.28.0 | cpu | 75/1151/2660/2159/0 | 23/479/1705/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261124 |
| v0.28.0 | rocm | 98/1377/2630/2563/0 | 23/480/1059/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261124 |
| v0.27.1 | gpu | 77/1170/2809/2241/0 | 24/479/1717/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261124 |
| v0.27.1 | cpu | 75/1154/2673/2159/0 | 23/479/1707/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261124 |
| v0.27.1 | rocm | 98/1378/2663/2572/0 | 23/480/1071/1148/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261124 |
| v0.27.0 | gpu | 77/1170/2809/2241/0 | 24/479/1717/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261124 |
| v0.27.0 | cpu | 75/1154/2673/2159/0 | 23/479/1707/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261124 |
| v0.27.0 | rocm | 98/1378/2663/2572/0 | 23/480/1071/1148/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261124 |
| v0.26.0 | gpu | 78/1176/2833/2243/0 | 24/479/1718/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261124 |
| v0.26.0 | cpu | 76/1160/2716/2166/0 | 23/479/1708/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261124 |
| v0.26.0 | rocm | 97/1374/2663/2571/0 | 23/480/1072/1148/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261124 |

<!-- scan-summary:end -->
