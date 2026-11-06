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

_Last scanned: 2026-11-06T08:01:58Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 15/387/2879/829/0 | 15/370/2842/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261106 |
| nightly | cpu | 18/488/1698/1138/0 | 18/479/1689/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261106 |
| nightly | rocm | 19/498/2281/1203/0 | 19/480/2263/1189/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261106 |
| v0.32.0 | gpu | 18/396/2888/835/0 | 15/370/2842/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261106 |
| v0.32.0 | cpu | 21/525/2666/1178/0 | 18/479/1689/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261106 |
| v0.32.0 | rocm | 51/823/3574/1629/0 | 19/480/1026/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261106 |
| v0.31.0 | gpu | 31/532/3767/983/0 | 16/372/2848/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261106 |
| v0.31.0 | cpu | 26/557/2724/1212/0 | 18/481/1695/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261106 |
| v0.31.0 | rocm | 51/830/3601/1650/0 | 19/482/1032/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261106 |
| v0.30.0 | gpu | 31/575/3999/1026/0 | 16/374/2849/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261106 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261106 |
| v0.30.0 | rocm | 51/833/3649/1651/0 | 19/484/1033/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261106 |
| v0.29.0 | gpu | 32/583/4132/1025/0 | 16/374/2856/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261106 |
| v0.29.0 | cpu | 32/657/3607/1307/0 | 18/483/1699/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261106 |
| v0.29.0 | rocm | 52/841/3701/1650/0 | 19/484/1040/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261106 |
| v0.28.0 | gpu | 32/594/4309/1036/0 | 16/374/2856/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261106 |
| v0.28.0 | cpu | 32/657/3665/1312/0 | 18/483/1699/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261106 |
| v0.28.0 | rocm | 51/841/3731/1652/0 | 18/484/1039/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261106 |
| v0.27.1 | gpu | 34/676/3789/1400/0 | 19/483/1692/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261106 |
| v0.27.1 | cpu | 32/660/3678/1312/0 | 18/483/1701/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261106 |
| v0.27.1 | rocm | 51/842/3755/1661/0 | 18/484/1041/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261106 |
| v0.27.0 | gpu | 34/676/3789/1400/0 | 19/483/1692/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261106 |
| v0.27.0 | cpu | 32/660/3678/1312/0 | 18/483/1701/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261106 |
| v0.27.0 | rocm | 51/842/3755/1661/0 | 18/484/1041/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261106 |
| v0.26.0 | gpu | 35/682/3813/1402/0 | 19/483/1693/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261106 |
| v0.26.0 | cpu | 33/666/3721/1319/0 | 18/483/1702/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261106 |
| v0.26.0 | rocm | 50/838/3755/1660/0 | 18/484/1042/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261106 |
| v0.25.1 | gpu | 39/808/4203/1655/0 | 19/483/1700/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261106 |
| v0.25.1 | cpu | 37/793/4115/1572/0 | 18/483/1709/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261106 |
| v0.25.1 | rocm | 50/849/3829/1664/0 | 18/484/1049/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261106 |

<!-- scan-summary:end -->
