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

_Last scanned: 2026-11-20T08:17:42Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 3/94/978/301/0 | 3/87/945/250/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261120 |
| nightly | cpu | 17/448/1508/1052/0 | 17/445/1500/1050/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261120 |
| nightly | rocm | 22/531/2230/1272/0 | 18/445/2088/1109/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261120 |
| v0.34.0 | gpu | 8/236/1202/572/0 | 3/87/955/251/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261120 |
| v0.34.0 | cpu | 19/519/1607/1208/0 | 17/445/1500/1050/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261120 |
| v0.34.0 | rocm | 22/532/2230/1272/0 | 18/446/2088/1109/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261120 |
| v0.33.0 | gpu | 42/771/1883/1598/0 | 3/87/955/251/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261120 |
| v0.33.0 | cpu | 21/528/1639/1215/0 | 17/445/1500/1050/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261120 |
| v0.33.0 | rocm | 40/808/1291/1732/0 | 18/446/844/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261120 |
| v0.32.0 | gpu | 45/776/1889/1598/0 | 3/87/955/251/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261120 |
| v0.32.0 | cpu | 41/806/1947/1683/0 | 17/445/1500/1050/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261120 |
| v0.32.0 | rocm | 92/1319/2257/2503/0 | 18/446/838/1098/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261120 |
| v0.31.0 | gpu | 68/1078/2263/2086/0 | 4/89/961/252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261120 |
| v0.31.0 | cpu | 46/847/2007/1717/0 | 17/447/1506/1051/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261120 |
| v0.31.0 | rocm | 92/1334/2285/2524/0 | 18/448/844/1099/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261120 |
| v0.30.0 | gpu | 73/1149/2417/2173/0 | 4/91/961/251/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261120 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261120 |
| v0.30.0 | rocm | 92/1337/2333/2525/0 | 18/450/845/1100/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261120 |
| v0.29.0 | gpu | 74/1157/2550/2172/0 | 4/91/968/252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261120 |
| v0.29.0 | cpu | 69/1119/2413/2101/0 | 17/449/1516/1049/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261120 |
| v0.29.0 | rocm | 93/1345/2385/2524/0 | 18/450/852/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261120 |
| v0.28.0 | gpu | 77/1182/2673/2221/0 | 4/91/968/252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261120 |
| v0.28.0 | cpu | 69/1120/2471/2106/0 | 17/449/1516/1049/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261120 |
| v0.28.0 | rocm | 92/1346/2415/2526/0 | 17/450/850/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261120 |
| v0.27.1 | gpu | 71/1139/2601/2201/0 | 18/449/1515/1096/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261120 |
| v0.27.1 | cpu | 69/1123/2484/2106/0 | 17/449/1518/1049/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261120 |
| v0.27.1 | rocm | 92/1347/2448/2535/0 | 17/450/862/1111/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261120 |
| v0.27.0 | gpu | 71/1139/2601/2201/0 | 18/449/1515/1096/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261120 |
| v0.27.0 | cpu | 69/1123/2484/2106/0 | 17/449/1518/1049/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261120 |
| v0.27.0 | rocm | 92/1347/2448/2535/0 | 17/450/862/1111/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261120 |
| v0.26.0 | gpu | 72/1145/2625/2203/0 | 18/449/1516/1097/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261120 |
| v0.26.0 | cpu | 70/1129/2527/2113/0 | 17/449/1519/1050/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261120 |
| v0.26.0 | rocm | 91/1343/2448/2534/0 | 17/450/863/1111/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261120 |

<!-- scan-summary:end -->
