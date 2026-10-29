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

_Last scanned: 2026-10-29T07:04:55Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/391/2775/835/0 | 14/372/2744/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261029 |
| nightly | cpu | 18/523/2577/1178/0 | 18/516/2575/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261029 |
| nightly | rocm | 19/525/1914/1221/0 | 19/517/1912/1220/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261029 |
| v0.32.0 | gpu | 17/392/2781/835/0 | 14/372/2744/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261029 |
| v0.32.0 | cpu | 20/524/2581/1178/0 | 18/516/2575/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261029 |
| v0.32.0 | rocm | 48/758/3725/1455/0 | 19/517/1913/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261029 |
| v0.31.0 | gpu | 30/528/3662/981/0 | 15/374/2750/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261029 |
| v0.31.0 | cpu | 25/556/2639/1212/0 | 18/518/2581/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261029 |
| v0.31.0 | rocm | 48/765/3752/1476/0 | 19/519/1919/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261029 |
| v0.30.0 | gpu | 30/571/3898/1020/0 | 15/376/2751/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261029 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/10/8/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261029 |
| v0.30.0 | rocm | 48/768/3800/1477/0 | 19/521/1920/1220/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261029 |
| v0.29.0 | gpu | 31/579/4031/1019/0 | 15/376/2758/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261029 |
| v0.29.0 | cpu | 30/653/3533/1300/0 | 18/520/2585/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261029 |
| v0.29.0 | rocm | 49/776/3852/1476/0 | 19/521/1927/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261029 |
| v0.28.0 | gpu | 31/590/4208/1030/0 | 15/376/2758/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261029 |
| v0.28.0 | cpu | 30/653/3591/1305/0 | 18/520/2585/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261029 |
| v0.28.0 | rocm | 48/776/3882/1478/0 | 18/521/1926/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261029 |
| v0.27.1 | gpu | 32/668/3717/1393/0 | 19/520/2580/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261029 |
| v0.27.1 | cpu | 30/656/3604/1305/0 | 18/520/2587/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261029 |
| v0.27.1 | rocm | 48/777/3906/1487/0 | 18/521/1928/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261029 |
| v0.27.0 | gpu | 32/668/3717/1393/0 | 19/520/2580/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261029 |
| v0.27.0 | cpu | 30/656/3604/1305/0 | 18/520/2587/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261029 |
| v0.27.0 | rocm | 48/777/3906/1487/0 | 18/521/1928/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261029 |
| v0.26.0 | gpu | 33/674/3741/1395/0 | 19/520/2581/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261029 |
| v0.26.0 | cpu | 31/662/3647/1312/0 | 18/520/2588/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261029 |
| v0.26.0 | rocm | 47/773/3906/1486/0 | 18/521/1929/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261029 |
| v0.25.1 | gpu | 36/749/4341/1490/0 | 19/520/2588/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261029 |
| v0.25.1 | cpu | 34/738/4251/1407/0 | 18/520/2595/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261029 |
| v0.25.1 | rocm | 47/784/3980/1490/0 | 18/521/1936/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261029 |
| v0.25.0 | gpu | 37/750/4342/1490/0 | 19/520/2588/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261029 |
| v0.25.0 | cpu | 35/739/4252/1407/0 | 18/520/2595/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261029 |
| v0.25.0 | rocm | 48/785/3981/1490/0 | 18/521/1936/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261029 |

<!-- scan-summary:end -->
