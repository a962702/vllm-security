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

_Last scanned: 2026-11-19T08:32:15Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 8/226/1192/548/0 | 8/219/1159/497/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261119 |
| nightly | cpu | 19/519/1607/1208/0 | 19/516/1599/1206/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261119 |
| nightly | rocm | 22/530/2231/1272/0 | 20/516/2187/1265/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261119 |
| v0.34.0 | gpu | 8/236/1196/572/0 | 8/219/1159/497/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.34.0-20261119 |
| v0.34.0 | cpu | 19/519/1607/1208/0 | 19/516/1599/1206/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.34.0-20261119 |
| v0.34.0 | rocm | 22/531/2231/1272/0 | 20/517/2187/1265/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.34.0-20261119 |
| v0.33.0 | gpu | 42/770/1878/1598/0 | 8/219/1159/497/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.33.0-20261119 |
| v0.33.0 | cpu | 21/527/1640/1215/0 | 19/516/1599/1206/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.33.0-20261119 |
| v0.33.0 | rocm | 40/807/1292/1732/0 | 20/517/943/1256/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.33.0-20261119 |
| v0.32.0 | gpu | 45/775/1884/1598/0 | 8/219/1159/497/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261119 |
| v0.32.0 | cpu | 41/805/1948/1683/0 | 19/516/1599/1206/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261119 |
| v0.32.0 | rocm | 92/1318/2258/2503/0 | 20/517/937/1254/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261119 |
| v0.31.0 | gpu | 68/1077/2258/2086/0 | 9/221/1165/498/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261119 |
| v0.31.0 | cpu | 46/846/2008/1717/0 | 19/518/1605/1207/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261119 |
| v0.31.0 | rocm | 92/1333/2286/2524/0 | 20/519/943/1255/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261119 |
| v0.30.0 | gpu | 73/1148/2412/2173/0 | 9/223/1165/497/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261119 |
| v0.30.0 | cpu | 7/50/47/13/0 | 0/4/8/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261119 |
| v0.30.0 | rocm | 92/1336/2334/2525/0 | 20/521/944/1256/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261119 |
| v0.29.0 | gpu | 74/1156/2545/2172/0 | 9/223/1172/498/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261119 |
| v0.29.0 | cpu | 69/1118/2414/2101/0 | 19/520/1614/1205/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261119 |
| v0.29.0 | rocm | 93/1344/2386/2524/0 | 20/521/951/1257/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261119 |
| v0.28.0 | gpu | 77/1180/2668/2221/0 | 9/223/1172/498/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261119 |
| v0.28.0 | cpu | 69/1118/2472/2106/0 | 19/520/1614/1205/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261119 |
| v0.28.0 | rocm | 92/1344/2416/2526/0 | 19/521/949/1257/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261119 |
| v0.27.1 | gpu | 71/1137/2602/2201/0 | 20/520/1614/1252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261119 |
| v0.27.1 | cpu | 69/1121/2485/2106/0 | 19/520/1616/1205/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261119 |
| v0.27.1 | rocm | 92/1345/2449/2535/0 | 19/521/961/1267/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261119 |
| v0.27.0 | gpu | 71/1137/2602/2201/0 | 20/520/1614/1252/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261119 |
| v0.27.0 | cpu | 69/1121/2485/2106/0 | 19/520/1616/1205/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261119 |
| v0.27.0 | rocm | 92/1345/2449/2535/0 | 19/521/961/1267/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261119 |
| v0.26.0 | gpu | 72/1143/2626/2203/0 | 20/520/1615/1253/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261119 |
| v0.26.0 | cpu | 70/1127/2528/2113/0 | 19/520/1617/1206/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261119 |
| v0.26.0 | rocm | 91/1341/2449/2534/0 | 19/521/962/1267/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261119 |

<!-- scan-summary:end -->
