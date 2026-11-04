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

_Last scanned: 2026-11-04T12:44:17Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 15/385/2843/829/0 | 15/370/2806/754/0 | ok | - |
| nightly | cpu | 18/477/1651/1124/0 | 18/470/1642/1122/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261104 |
| nightly | rocm | 19/486/2236/1189/0 | 19/471/2218/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261104 |
| v0.32.0 | gpu | 18/394/2852/835/0 | 15/370/2806/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261104 |
| v0.32.0 | cpu | 21/522/2632/1178/0 | 18/470/1642/1122/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261104 |
| v0.32.0 | rocm | 49/768/3751/1475/0 | 19/471/981/1164/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261104 |
| v0.31.0 | gpu | 31/530/3731/983/0 | 16/372/2812/755/0 | ok | - |
| v0.31.0 | cpu | 26/554/2690/1212/0 | 18/472/1648/1123/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261104 |
| v0.31.0 | rocm | 49/775/3778/1496/0 | 19/473/987/1165/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261104 |
| v0.30.0 | gpu | 31/573/3967/1022/0 | 16/374/2813/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261104 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261104 |
| v0.30.0 | rocm | 49/778/3826/1497/0 | 19/475/988/1166/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261104 |
| v0.29.0 | gpu | 32/581/4100/1021/0 | 16/374/2820/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261104 |
| v0.29.0 | cpu | 31/651/3581/1303/0 | 18/474/1652/1123/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261104 |
| v0.29.0 | rocm | 50/786/3878/1496/0 | 19/475/995/1167/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261104 |
| v0.28.0 | gpu | 32/592/4277/1032/0 | 16/374/2820/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261104 |
| v0.28.0 | cpu | 31/651/3639/1308/0 | 18/474/1652/1123/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261104 |
| v0.28.0 | rocm | 49/786/3908/1498/0 | 18/475/994/1167/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261104 |
| v0.27.1 | gpu | 33/670/3765/1396/0 | 19/474/1647/1163/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261104 |
| v0.27.1 | cpu | 31/654/3652/1308/0 | 18/474/1654/1123/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261104 |
| v0.27.1 | rocm | 49/787/3932/1507/0 | 18/475/996/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261104 |
| v0.27.0 | gpu | 33/670/3765/1396/0 | 19/474/1647/1163/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261104 |
| v0.27.0 | cpu | 31/654/3652/1308/0 | 18/474/1654/1123/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261104 |
| v0.27.0 | rocm | 49/787/3932/1507/0 | 18/475/996/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261104 |
| v0.26.0 | gpu | 34/676/3789/1398/0 | 19/474/1648/1164/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261104 |
| v0.26.0 | cpu | 32/660/3695/1315/0 | 18/474/1655/1124/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261104 |
| v0.26.0 | rocm | 48/783/3932/1506/0 | 18/475/997/1177/0 | ok | - |
| v0.25.1 | gpu | 37/758/4368/1509/0 | 19/474/1655/1164/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261104 |
| v0.25.1 | cpu | 35/743/4278/1426/0 | 18/474/1662/1124/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261104 |
| v0.25.1 | rocm | 48/794/4006/1510/0 | 18/475/1004/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261104 |

<!-- scan-summary:end -->
