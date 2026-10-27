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

_Last scanned: 2026-10-27T13:48:21Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/390/2620/829/0 | 14/372/2589/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261027 |
| nightly | cpu | 18/522/2446/1172/0 | 18/516/2444/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261027 |
| nightly | rocm | 19/523/1784/1215/0 | 19/517/1781/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261027 |
| v0.32.0 | gpu | 17/390/2623/829/0 | 14/372/2589/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261027 |
| v0.32.0 | cpu | 20/522/2447/1172/0 | 18/516/2444/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261027 |
| v0.32.0 | rocm | 48/756/3586/1449/0 | 19/517/1782/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261027 |
| v0.31.0 | gpu | 30/523/3484/973/0 | 15/372/2589/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261027 |
| v0.31.0 | cpu | 25/551/2485/1204/0 | 18/516/2444/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261027 |
| v0.31.0 | rocm | 48/760/3598/1468/0 | 19/517/1782/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261027 |
| v0.30.0 | gpu | 30/564/3719/1012/0 | 15/373/2590/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261027 |
| v0.30.0 | cpu | 7/35/26/5/0 | 0/1/2/1/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261027 |
| v0.30.0 | rocm | 48/761/3645/1469/0 | 19/518/1783/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261027 |
| v0.29.0 | gpu | 31/572/3853/1013/0 | 15/373/2597/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261027 |
| v0.29.0 | cpu | 30/647/3379/1294/0 | 18/517/2439/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261027 |
| v0.29.0 | rocm | 49/769/3698/1470/0 | 19/518/1790/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261027 |
| v0.28.0 | gpu | 31/583/4027/1025/0 | 15/373/2597/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261027 |
| v0.28.0 | cpu | 30/647/3434/1300/0 | 18/517/2439/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261027 |
| v0.28.0 | rocm | 48/769/3725/1473/0 | 18/518/1789/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261027 |
| v0.27.1 | gpu | 32/661/3560/1388/0 | 19/517/2443/1210/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261027 |
| v0.27.1 | cpu | 30/650/3447/1300/0 | 18/517/2441/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261027 |
| v0.27.1 | rocm | 48/770/3749/1482/0 | 18/518/1791/1224/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261027 |
| v0.27.0 | gpu | 32/661/3560/1388/0 | 19/517/2443/1210/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261027 |
| v0.27.0 | cpu | 30/650/3447/1300/0 | 18/517/2441/1170/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261027 |
| v0.27.0 | rocm | 48/770/3749/1482/0 | 18/518/1791/1224/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261027 |
| v0.26.0 | gpu | 33/668/3584/1390/0 | 19/517/2444/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261027 |
| v0.26.0 | cpu | 31/657/3490/1307/0 | 18/517/2442/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261027 |
| v0.26.0 | rocm | 47/767/3749/1481/0 | 18/518/1792/1224/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261027 |
| v0.25.1 | gpu | 36/744/4187/1485/0 | 19/517/2451/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261027 |
| v0.25.1 | cpu | 34/733/4097/1402/0 | 18/517/2449/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261027 |
| v0.25.1 | rocm | 47/778/3826/1485/0 | 18/518/1799/1224/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261027 |
| v0.25.0 | gpu | 37/745/4188/1485/0 | 19/517/2451/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261027 |
| v0.25.0 | cpu | 35/734/4098/1402/0 | 18/517/2449/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261027 |
| v0.25.0 | rocm | 48/779/3827/1485/0 | 18/518/1799/1224/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261027 |

<!-- scan-summary:end -->
