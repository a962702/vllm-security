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

_Last scanned: 2026-11-17T08:54:02Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/184/1237/460/0 | 5/177/1204/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261117 |
| nightly | cpu | 16/474/1696/1129/0 | 16/471/1689/1127/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261117 |
| nightly | rocm | 19/485/2309/1189/0 | 17/471/2265/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261117 |
| v0.34.0 | gpu | 5/194/1241/484/0 | 5/177/1204/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261117 |
| v0.34.0 | cpu | 16/474/1696/1129/0 | 16/471/1689/1127/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261117 |
| v0.34.0 | rocm | 19/486/2309/1189/0 | 17/472/2265/1182/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261117 |
| v0.33.0 | gpu | 30/617/2267/1286/0 | 5/177/1204/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261117 |
| v0.33.0 | cpu | 18/482/1729/1136/0 | 16/471/1689/1127/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261117 |
| v0.33.0 | rocm | 29/696/1574/1523/0 | 17/472/1025/1173/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261117 |
| v0.32.0 | gpu | 33/622/2273/1286/0 | 5/177/1204/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261117 |
| v0.32.0 | cpu | 30/694/2237/1478/0 | 16/471/1689/1127/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261117 |
| v0.32.0 | rocm | 81/1207/2550/2294/0 | 17/472/1030/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261117 |
| v0.31.0 | gpu | 56/924/2647/1774/0 | 6/179/1210/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261117 |
| v0.31.0 | cpu | 35/735/2297/1512/0 | 16/473/1695/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261117 |
| v0.31.0 | rocm | 81/1222/2578/2315/0 | 17/474/1036/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261117 |
| v0.30.0 | gpu | 61/995/2801/1861/0 | 6/181/1210/409/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261117 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261117 |
| v0.30.0 | rocm | 81/1225/2626/2316/0 | 17/476/1037/1173/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261117 |
| v0.29.0 | gpu | 62/1003/2934/1860/0 | 6/181/1217/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261117 |
| v0.29.0 | cpu | 58/1007/2688/1898/0 | 16/475/1688/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261117 |
| v0.29.0 | rocm | 82/1233/2678/2315/0 | 17/476/1044/1174/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261117 |
| v0.28.0 | gpu | 65/1027/3057/1909/0 | 6/181/1217/410/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261117 |
| v0.28.0 | cpu | 58/1007/2746/1903/0 | 16/475/1688/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261117 |
| v0.28.0 | rocm | 81/1233/2708/2317/0 | 16/476/1042/1174/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261117 |
| v0.27.1 | gpu | 60/1026/2881/1991/0 | 17/475/1693/1168/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261117 |
| v0.27.1 | cpu | 58/1010/2759/1903/0 | 16/475/1690/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261117 |
| v0.27.1 | rocm | 81/1234/2732/2326/0 | 16/476/1044/1184/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261117 |
| v0.27.0 | gpu | 60/1026/2881/1991/0 | 17/475/1693/1168/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261117 |
| v0.27.0 | cpu | 58/1010/2759/1903/0 | 16/475/1690/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261117 |
| v0.27.0 | rocm | 81/1234/2732/2326/0 | 16/476/1044/1184/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261117 |
| v0.26.0 | gpu | 61/1032/2905/1993/0 | 17/475/1694/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261117 |
| v0.26.0 | cpu | 59/1016/2802/1910/0 | 16/475/1691/1129/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261117 |
| v0.26.0 | rocm | 80/1230/2732/2325/0 | 16/476/1045/1184/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261117 |

<!-- scan-summary:end -->
