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

_Last scanned: 2026-10-30T07:05:38Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/391/2847/835/0 | 14/372/2816/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261030 |
| nightly | cpu | 18/523/2629/1178/0 | 18/516/2627/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261030 |
| nightly | rocm | 19/528/3208/1237/0 | 19/517/3199/1229/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261030 |
| v0.32.0 | gpu | 17/392/2853/835/0 | 14/372/2816/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261030 |
| v0.32.0 | cpu | 20/524/2633/1178/0 | 18/516/2627/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261030 |
| v0.32.0 | rocm | 48/758/3770/1463/0 | 19/517/1966/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261030 |
| v0.31.0 | gpu | 30/528/3734/981/0 | 15/374/2822/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261030 |
| v0.31.0 | cpu | 25/556/2691/1212/0 | 18/518/2633/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261030 |
| v0.31.0 | rocm | 48/765/3797/1484/0 | 19/519/1972/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261030 |
| v0.30.0 | gpu | 30/571/3970/1020/0 | 15/376/2823/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261030 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/10/8/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261030 |
| v0.30.0 | rocm | 48/768/3845/1485/0 | 19/521/1973/1220/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261030 |
| v0.29.0 | gpu | 31/579/4103/1019/0 | 15/376/2830/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261030 |
| v0.29.0 | cpu | 30/653/3585/1300/0 | 18/520/2637/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261030 |
| v0.29.0 | rocm | 49/776/3897/1484/0 | 19/521/1980/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261030 |
| v0.28.0 | gpu | 31/590/4280/1030/0 | 15/376/2830/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261030 |
| v0.28.0 | cpu | 30/653/3643/1305/0 | 18/520/2637/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261030 |
| v0.28.0 | rocm | 48/776/3927/1486/0 | 18/521/1979/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261030 |
| v0.27.1 | gpu | 32/668/3769/1393/0 | 19/520/2632/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261030 |
| v0.27.1 | cpu | 30/656/3656/1305/0 | 18/520/2639/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261030 |
| v0.27.1 | rocm | 48/777/3951/1495/0 | 18/521/1981/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261030 |
| v0.27.0 | gpu | 32/668/3769/1393/0 | 19/520/2632/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261030 |
| v0.27.0 | cpu | 30/656/3656/1305/0 | 18/520/2639/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261030 |
| v0.27.0 | rocm | 48/777/3951/1495/0 | 18/521/1981/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261030 |
| v0.26.0 | gpu | 33/674/3793/1395/0 | 19/520/2633/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261030 |
| v0.26.0 | cpu | 31/662/3699/1312/0 | 18/520/2640/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261030 |
| v0.26.0 | rocm | 47/773/3951/1494/0 | 18/521/1982/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261030 |
| v0.25.1 | gpu | 36/749/4385/1498/0 | 19/520/2640/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261030 |
| v0.25.1 | cpu | 34/738/4295/1415/0 | 18/520/2647/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261030 |
| v0.25.1 | rocm | 47/784/4025/1498/0 | 18/521/1989/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261030 |
| v0.25.0 | gpu | 37/750/4386/1498/0 | 19/520/2640/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261030 |
| v0.25.0 | cpu | 35/739/4296/1415/0 | 18/520/2647/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261030 |
| v0.25.0 | rocm | 48/785/4026/1498/0 | 18/521/1989/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261030 |

<!-- scan-summary:end -->
