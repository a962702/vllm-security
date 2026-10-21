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

_Last scanned: 2026-10-21T05:52:10Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 16/390/2620/827/0 | 16/376/2591/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261021 |
| nightly | cpu | 19/522/2446/1170/0 | 19/522/2446/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261021 |
| nightly | rocm | 21/529/1792/1213/0 | 21/529/1792/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261021 |
| v0.32.0 | gpu | 17/390/2620/827/0 | 17/376/2591/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261021 |
| v0.32.0 | cpu | 20/522/2446/1170/0 | 20/522/2446/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261021 |
| v0.32.0 | rocm | 44/737/3587/1443/0 | 22/529/1793/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261021 |
| v0.31.0 | gpu | 26/505/3469/970/0 | 19/385/2596/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261021 |
| v0.31.0 | cpu | 21/533/2471/1201/0 | 21/532/2451/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261021 |
| v0.31.0 | rocm | 44/740/3598/1461/0 | 22/532/1796/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261021 |
| v0.30.0 | gpu | 26/545/3703/1009/0 | 19/385/2601/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261021 |
| v0.30.0 | cpu | 3/16/12/2/0 | 3/16/12/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261021 |
| v0.30.0 | rocm | 44/740/3644/1462/0 | 22/532/1801/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261021 |
| v0.29.0 | gpu | 27/552/3837/1010/0 | 20/392/2618/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261021 |
| v0.29.0 | cpu | 26/627/3364/1291/0 | 22/539/2459/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261021 |
| v0.29.0 | rocm | 45/747/3697/1463/0 | 23/539/1818/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261021 |
| v0.28.0 | gpu | 27/563/4011/1022/0 | 20/392/2616/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261021 |
| v0.28.0 | cpu | 26/627/3419/1297/0 | 22/539/2458/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261021 |
| v0.28.0 | rocm | 44/747/3724/1466/0 | 22/539/1817/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261021 |
| v0.27.1 | gpu | 28/641/3544/1385/0 | 24/537/2462/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261021 |
| v0.27.1 | cpu | 26/630/3432/1297/0 | 22/540/2462/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261021 |
| v0.27.1 | rocm | 44/748/3748/1475/0 | 22/540/1821/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261021 |
| v0.27.0 | gpu | 28/641/3544/1385/0 | 24/537/2462/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261021 |
| v0.27.0 | cpu | 26/630/3432/1297/0 | 22/540/2462/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261021 |
| v0.27.0 | rocm | 44/748/3748/1475/0 | 22/540/1821/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261021 |
| v0.26.0 | gpu | 29/648/3568/1388/0 | 23/533/2460/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261021 |
| v0.26.0 | cpu | 27/637/3475/1305/0 | 21/536/2462/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261021 |
| v0.26.0 | rocm | 43/745/3748/1475/0 | 21/537/1821/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261021 |
| v0.25.1 | gpu | 32/723/4176/1479/0 | 23/534/2469/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261021 |
| v0.25.1 | cpu | 30/712/4087/1396/0 | 21/537/2471/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261021 |
| v0.25.1 | rocm | 43/756/3825/1479/0 | 21/548/1833/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261021 |
| v0.25.0 | gpu | 33/724/4177/1479/0 | 24/535/2470/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261021 |
| v0.25.0 | cpu | 31/713/4088/1396/0 | 22/538/2472/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261021 |
| v0.25.0 | rocm | 44/757/3826/1479/0 | 22/549/1834/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261021 |

<!-- scan-summary:end -->
