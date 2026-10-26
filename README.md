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

_Last scanned: 2026-10-26T05:46:26Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | - | - | scan_failed | - |
| nightly | cpu | - | - | scan_failed | - |
| nightly | rocm | - | - | scan_failed | - |
| v0.32.0 | gpu | - | - | scan_failed | - |
| v0.32.0 | cpu | 20/522/2446/1172/0 | 20/522/2446/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261026 |
| v0.32.0 | rocm | 48/755/3586/1449/0 | 26/546/1797/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261026 |
| v0.31.0 | gpu | - | - | scan_failed | - |
| v0.31.0 | cpu | - | - | scan_failed | - |
| v0.31.0 | rocm | 48/759/3597/1469/0 | 26/550/1800/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261026 |
| v0.30.0 | gpu | - | - | scan_failed | - |
| v0.30.0 | cpu | - | - | scan_failed | - |
| v0.30.0 | rocm | 48/760/3644/1470/0 | 26/551/1806/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261026 |
| v0.29.0 | gpu | 31/572/3851/1014/0 | 24/412/2630/759/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261026 |
| v0.29.0 | cpu | - | - | scan_failed | - |
| v0.29.0 | rocm | 49/768/3697/1471/0 | 27/559/1823/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261026 |
| v0.28.0 | gpu | - | - | scan_failed | - |
| v0.28.0 | cpu | - | - | scan_failed | - |
| v0.28.0 | rocm | 48/768/3724/1474/0 | 26/559/1822/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261026 |
| v0.27.1 | gpu | 32/661/3558/1389/0 | 28/557/2476/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261026 |
| v0.27.1 | cpu | - | - | scan_failed | - |
| v0.27.1 | rocm | 48/769/3748/1483/0 | 26/560/1826/1229/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261026 |
| v0.27.0 | gpu | 32/661/3558/1389/0 | 28/557/2476/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261026 |
| v0.27.0 | cpu | - | - | scan_failed | - |
| v0.27.0 | rocm | - | - | scan_failed | - |
| v0.26.0 | gpu | 33/668/3582/1391/0 | 27/553/2474/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261026 |
| v0.26.0 | cpu | - | - | scan_failed | - |
| v0.26.0 | rocm | - | - | scan_failed | - |
| v0.25.1 | gpu | - | - | scan_failed | - |
| v0.25.1 | cpu | - | - | scan_failed | - |
| v0.25.1 | rocm | 47/777/3825/1486/0 | 25/568/1838/1228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261026 |
| v0.25.0 | gpu | - | - | scan_failed | - |
| v0.25.0 | cpu | 35/733/4097/1403/0 | 26/558/2485/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261026 |
| v0.25.0 | rocm | - | - | scan_failed | - |

<!-- scan-summary:end -->
