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

_Last scanned: 2026-11-10T08:11:16Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 20/436/2783/875/0 | 20/419/2746/800/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261110 |
| nightly | cpu | 18/488/1693/1137/0 | 18/479/1684/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261110 |
| nightly | rocm | 19/492/2261/1195/0 | 19/480/2252/1189/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261110 |
| v0.32.0 | gpu | 23/445/2792/881/0 | 20/419/2746/800/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261110 |
| v0.32.0 | cpu | 22/553/2596/1212/0 | 18/479/1684/1135/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261110 |
| v0.32.0 | rocm | 72/1055/2937/2010/0 | 19/480/1024/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261110 |
| v0.31.0 | gpu | 46/733/3179/1359/0 | 21/421/2752/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261110 |
| v0.31.0 | cpu | 27/585/2654/1246/0 | 18/481/1690/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261110 |
| v0.31.0 | rocm | 72/1062/2964/2031/0 | 19/482/1030/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261110 |
| v0.30.0 | gpu | 51/804/3334/1446/0 | 21/423/2753/800/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261110 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261110 |
| v0.30.0 | rocm | 72/1065/3012/2032/0 | 19/484/1031/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261110 |
| v0.29.0 | gpu | 52/812/3467/1445/0 | 21/423/2760/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261110 |
| v0.29.0 | cpu | 49/847/3079/1614/0 | 18/483/1688/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261110 |
| v0.29.0 | rocm | 73/1073/3064/2031/0 | 19/484/1038/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261110 |
| v0.28.0 | gpu | 55/836/3590/1494/0 | 21/423/2760/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261110 |
| v0.28.0 | cpu | 49/847/3137/1619/0 | 18/483/1688/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261110 |
| v0.28.0 | rocm | 72/1073/3094/2033/0 | 18/484/1037/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261110 |
| v0.27.1 | gpu | 51/866/3267/1707/0 | 19/483/1687/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261110 |
| v0.27.1 | cpu | 49/850/3150/1619/0 | 18/483/1690/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261110 |
| v0.27.1 | rocm | 72/1074/3118/2042/0 | 18/484/1039/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261110 |
| v0.27.0 | gpu | 51/866/3267/1707/0 | 19/483/1687/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261110 |
| v0.27.0 | cpu | 49/850/3150/1619/0 | 18/483/1690/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261110 |
| v0.27.0 | rocm | 72/1074/3118/2042/0 | 18/484/1039/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261110 |
| v0.26.0 | gpu | 52/872/3291/1709/0 | 19/483/1688/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261110 |
| v0.26.0 | cpu | 50/856/3193/1626/0 | 18/483/1691/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261110 |
| v0.26.0 | rocm | 71/1070/3118/2041/0 | 18/484/1040/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261110 |
| v0.25.1 | gpu | 60/1040/3564/2033/0 | 19/483/1695/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261110 |
| v0.25.1 | cpu | 58/1025/3470/1950/0 | 18/483/1698/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261110 |
| v0.25.1 | rocm | 71/1081/3192/2045/0 | 18/484/1047/1192/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261110 |

<!-- scan-summary:end -->
