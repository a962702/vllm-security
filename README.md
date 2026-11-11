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

_Last scanned: 2026-11-11T07:32:03Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 20/436/2811/876/0 | 20/419/2774/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261111 |
| nightly | cpu | 18/488/1700/1138/0 | 18/479/1691/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261111 |
| nightly | rocm | 19/492/2273/1197/0 | 19/480/2264/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261111 |
| v0.32.0 | gpu | 23/445/2820/882/0 | 20/419/2774/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261111 |
| v0.32.0 | cpu | 22/553/2603/1213/0 | 18/479/1691/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261111 |
| v0.32.0 | rocm | 72/1055/2941/2011/0 | 19/480/1028/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261111 |
| v0.31.0 | gpu | 46/733/3207/1360/0 | 21/421/2780/802/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261111 |
| v0.31.0 | cpu | 27/585/2661/1247/0 | 18/481/1697/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261111 |
| v0.31.0 | rocm | 72/1062/2968/2032/0 | 19/482/1034/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261111 |
| v0.30.0 | gpu | 51/804/3361/1447/0 | 21/423/2780/801/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261111 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261111 |
| v0.30.0 | rocm | 72/1065/3016/2033/0 | 19/484/1035/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261111 |
| v0.29.0 | gpu | 52/812/3494/1446/0 | 21/423/2787/802/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261111 |
| v0.29.0 | cpu | 49/847/3085/1615/0 | 18/483/1694/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261111 |
| v0.29.0 | rocm | 73/1073/3068/2032/0 | 19/484/1042/1183/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261111 |
| v0.28.0 | gpu | 55/836/3617/1495/0 | 21/423/2787/802/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261111 |
| v0.28.0 | cpu | 49/847/3143/1620/0 | 18/483/1694/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261111 |
| v0.28.0 | rocm | 72/1073/3098/2034/0 | 18/484/1041/1183/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261111 |
| v0.27.1 | gpu | 51/866/3274/1708/0 | 19/483/1694/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261111 |
| v0.27.1 | cpu | 49/850/3156/1620/0 | 18/483/1696/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261111 |
| v0.27.1 | rocm | 72/1074/3122/2043/0 | 18/484/1043/1193/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261111 |
| v0.27.0 | gpu | 51/866/3274/1708/0 | 19/483/1694/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261111 |
| v0.27.0 | cpu | 49/850/3156/1620/0 | 18/483/1696/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261111 |
| v0.27.0 | rocm | 72/1074/3122/2043/0 | 18/484/1043/1193/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261111 |
| v0.26.0 | gpu | 52/872/3298/1710/0 | 19/483/1695/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261111 |
| v0.26.0 | cpu | 50/856/3199/1627/0 | 18/483/1697/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261111 |
| v0.26.0 | rocm | 71/1070/3122/2042/0 | 18/484/1044/1193/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261111 |
| v0.25.1 | gpu | 60/1040/3571/2034/0 | 19/483/1702/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261111 |
| v0.25.1 | cpu | 58/1025/3476/1951/0 | 18/483/1704/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261111 |
| v0.25.1 | rocm | 71/1081/3196/2046/0 | 18/484/1051/1193/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261111 |

<!-- scan-summary:end -->
