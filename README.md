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

_Last scanned: 2026-11-28T16:16:22Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 13/192/1180/379/0 | 13/185/1147/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261128 |
| nightly | cpu | 26/527/1716/1102/0 | 26/524/1646/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261128 |
| nightly | rocm | 26/537/2461/1175/0 | 26/524/2272/1140/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261128 |
| v0.34.0 | gpu | 18/334/1637/662/0 | 13/185/1160/329/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261128 |
| v0.34.0 | cpu | 28/598/1921/1287/0 | 26/524/1646/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261128 |
| v0.34.0 | rocm | 31/611/2590/1332/0 | 27/525/2272/1140/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261128 |
| v0.33.0 | gpu | 52/870/2318/1688/0 | 13/185/1160/329/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261128 |
| v0.33.0 | cpu | 30/607/1953/1294/0 | 26/524/1646/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261128 |
| v0.33.0 | rocm | 49/888/1637/1790/0 | 27/525/1021/1130/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261128 |
| v0.32.0 | gpu | 55/875/2324/1688/0 | 13/185/1160/329/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261128 |
| v0.32.0 | cpu | 50/886/2261/1762/0 | 26/524/1646/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261128 |
| v0.32.0 | rocm | 101/1399/2605/2562/0 | 27/525/1018/1127/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261128 |
| v0.31.0 | gpu | 78/1177/2699/2176/0 | 14/187/1166/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261128 |
| v0.31.0 | cpu | 55/927/2322/1796/0 | 26/526/1652/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261128 |
| v0.31.0 | rocm | 101/1414/2633/2583/0 | 27/527/1024/1128/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261128 |
| v0.30.0 | gpu | 83/1248/2853/2263/0 | 14/189/1166/329/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261128 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261128 |
| v0.30.0 | rocm | 101/1417/2681/2584/0 | 27/529/1025/1129/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261128 |
| v0.29.0 | gpu | 84/1256/2986/2262/0 | 14/189/1173/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261128 |
| v0.29.0 | cpu | 78/1199/2715/2178/0 | 26/528/1657/1099/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261128 |
| v0.29.0 | rocm | 102/1425/2733/2583/0 | 27/529/1032/1130/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261128 |
| v0.28.0 | gpu | 87/1281/3109/2311/0 | 14/189/1173/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261128 |
| v0.28.0 | cpu | 78/1200/2773/2183/0 | 26/528/1657/1099/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261128 |
| v0.28.0 | rocm | 101/1426/2763/2585/0 | 26/529/1030/1130/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261128 |
| v0.27.1 | gpu | 80/1219/2932/2264/0 | 27/528/1669/1130/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261128 |
| v0.27.1 | cpu | 78/1203/2786/2183/0 | 26/528/1659/1099/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261128 |
| v0.27.1 | rocm | 101/1427/2796/2594/0 | 26/529/1042/1140/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261128 |
| v0.27.0 | gpu | 80/1219/2932/2264/0 | 27/528/1669/1130/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261128 |
| v0.27.0 | cpu | 78/1203/2786/2183/0 | 26/528/1659/1099/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261128 |
| v0.27.0 | rocm | 101/1427/2796/2594/0 | 26/529/1042/1140/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261128 |
| v0.26.0 | gpu | 81/1225/2956/2266/0 | 27/528/1670/1131/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261128 |
| v0.26.0 | cpu | 79/1209/2829/2190/0 | 26/528/1660/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261128 |
| v0.26.0 | rocm | 100/1423/2796/2593/0 | 26/529/1043/1140/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261128 |

<!-- scan-summary:end -->
