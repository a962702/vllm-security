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

_Last scanned: 2026-11-05T08:13:01Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 15/387/2875/829/0 | 15/372/2838/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261105 |
| nightly | cpu | 18/488/1694/1138/0 | 18/481/1685/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261105 |
| nightly | rocm | 19/498/2277/1203/0 | 19/483/2259/1189/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261105 |
| v0.32.0 | gpu | 18/396/2884/835/0 | 15/372/2838/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261105 |
| v0.32.0 | cpu | 21/525/2662/1178/0 | 18/481/1685/1136/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261105 |
| v0.32.0 | rocm | 51/806/3684/1532/0 | 19/483/1022/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261105 |
| v0.31.0 | gpu | 31/532/3763/983/0 | 16/374/2844/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261105 |
| v0.31.0 | cpu | 26/557/2720/1212/0 | 18/483/1691/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261105 |
| v0.31.0 | rocm | 51/813/3711/1553/0 | 19/485/1028/1179/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261105 |
| v0.30.0 | gpu | 31/575/3999/1022/0 | 16/376/2845/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261105 |
| v0.30.0 | cpu | 7/40/44/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261105 |
| v0.30.0 | rocm | 51/816/3759/1554/0 | 19/487/1029/1180/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261105 |
| v0.29.0 | gpu | 32/583/4132/1021/0 | 16/376/2852/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261105 |
| v0.29.0 | cpu | 32/656/3607/1304/0 | 18/485/1695/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261105 |
| v0.29.0 | rocm | 52/824/3811/1553/0 | 19/487/1036/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261105 |
| v0.28.0 | gpu | 32/594/4309/1032/0 | 16/376/2852/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261105 |
| v0.28.0 | cpu | 32/656/3665/1309/0 | 18/485/1695/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261105 |
| v0.28.0 | rocm | 51/824/3841/1555/0 | 18/487/1035/1181/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261105 |
| v0.27.1 | gpu | 34/675/3789/1397/0 | 19/485/1688/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261105 |
| v0.27.1 | cpu | 32/659/3678/1309/0 | 18/485/1697/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261105 |
| v0.27.1 | rocm | 51/825/3865/1564/0 | 18/487/1037/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261105 |
| v0.27.0 | gpu | 34/675/3789/1397/0 | 19/485/1688/1177/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261105 |
| v0.27.0 | cpu | 32/659/3678/1309/0 | 18/485/1697/1137/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261105 |
| v0.27.0 | rocm | 51/825/3865/1564/0 | 18/487/1037/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261105 |
| v0.26.0 | gpu | 35/681/3813/1399/0 | 19/485/1689/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261105 |
| v0.26.0 | cpu | 33/665/3721/1316/0 | 18/485/1698/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261105 |
| v0.26.0 | rocm | 50/821/3865/1563/0 | 18/487/1038/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261105 |
| v0.25.1 | gpu | 39/791/4313/1558/0 | 19/485/1696/1178/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261105 |
| v0.25.1 | cpu | 37/776/4225/1475/0 | 18/485/1705/1138/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261105 |
| v0.25.1 | rocm | 50/832/3939/1567/0 | 18/487/1045/1191/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261105 |

<!-- scan-summary:end -->
