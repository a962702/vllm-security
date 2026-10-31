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

_Last scanned: 2026-10-31T06:50:35Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/390/2847/835/0 | 14/371/2816/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261031 |
| nightly | cpu | 18/522/2629/1178/0 | 18/515/2627/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261031 |
| nightly | rocm | 19/531/3212/1237/0 | 19/516/3203/1229/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261031 |
| v0.32.0 | gpu | 17/395/2853/835/0 | 14/371/2816/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261031 |
| v0.32.0 | cpu | 20/523/2633/1178/0 | 18/515/2627/1176/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261031 |
| v0.32.0 | rocm | 48/762/3767/1467/0 | 19/516/1966/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261031 |
| v0.31.0 | gpu | 30/531/3733/982/0 | 15/373/2822/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261031 |
| v0.31.0 | cpu | 25/555/2691/1212/0 | 18/517/2633/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261031 |
| v0.31.0 | rocm | 48/769/3794/1488/0 | 19/518/1972/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261031 |
| v0.30.0 | gpu | 30/574/3969/1021/0 | 15/375/2823/760/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261031 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/10/8/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261031 |
| v0.30.0 | rocm | 48/772/3842/1489/0 | 19/520/1973/1220/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261031 |
| v0.29.0 | gpu | 31/582/4102/1020/0 | 15/375/2830/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261031 |
| v0.29.0 | cpu | 30/652/3583/1302/0 | 18/519/2637/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261031 |
| v0.29.0 | rocm | 49/780/3894/1488/0 | 19/520/1980/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261031 |
| v0.28.0 | gpu | 31/593/4279/1031/0 | 15/375/2830/761/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261031 |
| v0.28.0 | cpu | 30/652/3641/1307/0 | 18/519/2637/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261031 |
| v0.28.0 | rocm | 48/780/3924/1490/0 | 18/520/1979/1221/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261031 |
| v0.27.1 | gpu | 32/671/3767/1395/0 | 19/519/2632/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261031 |
| v0.27.1 | cpu | 30/655/3654/1307/0 | 18/519/2639/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261031 |
| v0.27.1 | rocm | 48/781/3948/1499/0 | 18/520/1981/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261031 |
| v0.27.0 | gpu | 32/671/3767/1395/0 | 19/519/2632/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261031 |
| v0.27.0 | cpu | 30/655/3654/1307/0 | 18/519/2639/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261031 |
| v0.27.0 | rocm | 48/781/3948/1499/0 | 18/520/1981/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261031 |
| v0.26.0 | gpu | 33/677/3791/1397/0 | 19/519/2633/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261031 |
| v0.26.0 | cpu | 31/661/3697/1314/0 | 18/519/2640/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261031 |
| v0.26.0 | rocm | 47/777/3948/1498/0 | 18/520/1982/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261031 |
| v0.25.1 | gpu | 36/753/4382/1502/0 | 19/519/2640/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261031 |
| v0.25.1 | cpu | 34/738/4292/1419/0 | 18/519/2647/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261031 |
| v0.25.1 | rocm | 47/788/4022/1502/0 | 18/520/1989/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261031 |
| v0.25.0 | gpu | - | - | scan_failed | - |
| v0.25.0 | cpu | 35/739/4293/1419/0 | 18/519/2647/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261031 |
| v0.25.0 | rocm | 48/789/4023/1502/0 | 18/520/1989/1231/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261031 |

<!-- scan-summary:end -->
