# vLLM Image Security Scanner

Automated daily security scanning of the official [vLLM](https://github.com/vllm-project/vllm)
Docker images. Each day this pipeline:

1. Finds the last 10 non-prerelease vLLM releases.
2. Scans every published image variant (`gpu`, `cpu`, `rocm`) with
   [Trivy](https://github.com/aquasecurity/trivy) — OS packages and Python
   packages.
3. Attempts an in-place `apt-get upgrade` + `pip install --upgrade` patch,
   and rescans the result.
4. Publishes the before/after vulnerability counts and pushes patched
   images to `ghcr.io/<owner>/vllm-security/<image-name>:<version>-<scan-date>`
   (e.g. `vllm-openai`, `vllm-openai-cpu`, `vllm-openai-rocm`; scan-date is a
   UTC `YYYYMMDD` stamp).

Full dashboard with historical trends: see the GitHub Pages site linked
below once the first scan has run. The dashboard also lets you pick any of
the last 7 scanned days and drill into the complete per-image vulnerability
report (not just counts).

Patched images are best-effort security-metrics artifacts, not supported
vLLM builds — functional correctness is not guaranteed.

## Latest Scan Summary

<!-- scan-summary:start -->

_Last scanned: 2026-10-24T05:37:37Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/390/2620/829/0 | 14/376/2591/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261024 |
| nightly | cpu | 18/522/2446/1172/0 | 18/522/2446/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261024 |
| nightly | rocm | - | - | scan_failed | - |
| v0.32.0 | gpu | 17/390/2622/829/0 | 17/376/2591/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261024 |
| v0.32.0 | cpu | 20/522/2446/1172/0 | 20/522/2446/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261024 |
| v0.32.0 | rocm | 48/755/3586/1449/0 | 26/546/1797/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261024 |
| v0.31.0 | gpu | 30/523/3482/974/0 | 23/403/2607/759/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261024 |
| v0.31.0 | cpu | 25/551/2483/1205/0 | 25/550/2463/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261024 |
| v0.31.0 | rocm | 48/759/3597/1469/0 | 26/550/1800/1217/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261024 |
| v0.30.0 | gpu | 30/564/3717/1013/0 | 23/404/2613/758/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261024 |
| v0.30.0 | cpu | 7/35/25/6/0 | 7/35/25/6/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261024 |
| v0.30.0 | rocm | 48/760/3644/1470/0 | 26/551/1806/1218/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261024 |
| v0.29.0 | gpu | 31/572/3851/1014/0 | 24/412/2630/759/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261024 |
| v0.29.0 | cpu | 30/647/3377/1295/0 | 26/559/2472/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261024 |
| v0.29.0 | rocm | 49/768/3697/1471/0 | 27/559/1823/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261024 |
| v0.28.0 | gpu | 31/583/4025/1026/0 | 24/412/2628/759/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261024 |
| v0.28.0 | cpu | 30/647/3432/1301/0 | 26/559/2471/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261024 |
| v0.28.0 | rocm | 48/768/3724/1474/0 | 26/559/1822/1219/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261024 |
| v0.27.1 | gpu | 32/661/3558/1389/0 | 28/557/2476/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261024 |
| v0.27.1 | cpu | 30/650/3445/1301/0 | 26/560/2475/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261024 |
| v0.27.1 | rocm | 48/769/3748/1483/0 | 26/560/1826/1229/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261024 |
| v0.27.0 | gpu | 32/661/3558/1389/0 | 28/557/2476/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261024 |
| v0.27.0 | cpu | 30/650/3445/1301/0 | 26/560/2475/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261024 |
| v0.27.0 | rocm | 48/769/3748/1483/0 | 26/560/1826/1229/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261024 |
| v0.26.0 | gpu | 33/668/3582/1391/0 | 27/553/2474/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261024 |
| v0.26.0 | cpu | 31/657/3488/1308/0 | 25/556/2475/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261024 |
| v0.26.0 | rocm | 47/766/3748/1482/0 | 25/557/1826/1228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261024 |
| v0.25.1 | gpu | 36/743/4186/1486/0 | 27/554/2483/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261024 |
| v0.25.1 | cpu | 34/732/4096/1403/0 | 25/557/2484/1175/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261024 |
| v0.25.1 | rocm | 47/777/3825/1486/0 | 25/568/1838/1228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261024 |
| v0.25.0 | gpu | 37/744/4187/1486/0 | 28/555/2484/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261024 |
| v0.25.0 | cpu | - | - | scan_failed | - |
| v0.25.0 | rocm | 48/778/3826/1486/0 | 26/569/1839/1228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261024 |

<!-- scan-summary:end -->
