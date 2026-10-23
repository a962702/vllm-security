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

_Last scanned: 2026-10-23T05:59:46Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/390/2622/827/0 | 14/376/2593/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261023 |
| nightly | cpu | 18/522/2445/1170/0 | 18/522/2445/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261023 |
| nightly | rocm | 23/546/1794/1213/0 | 23/546/1794/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261023 |
| v0.32.0 | gpu | 17/390/2622/827/0 | 17/376/2593/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261023 |
| v0.32.0 | cpu | 20/522/2445/1170/0 | 20/522/2445/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261023 |
| v0.32.0 | rocm | 47/754/3589/1443/0 | 25/546/1795/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261023 |
| v0.31.0 | gpu | 29/522/3481/970/0 | 22/402/2608/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261023 |
| v0.31.0 | cpu | 24/550/2481/1201/0 | 24/549/2461/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261023 |
| v0.31.0 | rocm | 47/757/3600/1461/0 | 25/549/1798/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261023 |
| v0.30.0 | gpu | 29/562/3715/1009/0 | 22/402/2613/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261023 |
| v0.30.0 | cpu | 6/33/23/2/0 | 6/33/23/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261023 |
| v0.30.0 | rocm | 47/757/3646/1462/0 | 25/549/1803/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261023 |
| v0.29.0 | gpu | 30/570/3849/1010/0 | 23/410/2630/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261023 |
| v0.29.0 | cpu | 29/645/3374/1291/0 | 25/557/2469/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261023 |
| v0.29.0 | rocm | 48/765/3699/1463/0 | 26/557/1820/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261023 |
| v0.28.0 | gpu | 30/581/4023/1022/0 | 23/410/2628/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261023 |
| v0.28.0 | cpu | 29/645/3429/1297/0 | 25/557/2468/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261023 |
| v0.28.0 | rocm | 47/765/3726/1466/0 | 25/557/1819/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261023 |
| v0.27.1 | gpu | 31/659/3555/1385/0 | 27/555/2473/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261023 |
| v0.27.1 | cpu | 29/648/3442/1297/0 | 25/558/2472/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261023 |
| v0.27.1 | rocm | 47/766/3750/1475/0 | 25/558/1823/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261023 |
| v0.27.0 | gpu | 31/659/3555/1385/0 | 27/555/2473/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261023 |
| v0.27.0 | cpu | 29/648/3442/1297/0 | 25/558/2472/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261023 |
| v0.27.0 | rocm | 47/766/3750/1475/0 | 25/558/1823/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261023 |
| v0.26.0 | gpu | 32/666/3579/1388/0 | 26/551/2471/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261023 |
| v0.26.0 | cpu | 30/655/3485/1305/0 | 24/554/2472/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261023 |
| v0.26.0 | rocm | 46/763/3750/1475/0 | 24/555/1823/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261023 |
| v0.25.1 | gpu | 35/741/4187/1479/0 | 26/552/2480/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261023 |
| v0.25.1 | cpu | 33/730/4097/1396/0 | 24/555/2481/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261023 |
| v0.25.1 | rocm | 46/774/3827/1479/0 | 24/566/1835/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261023 |
| v0.25.0 | gpu | 36/742/4188/1479/0 | 27/553/2481/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261023 |
| v0.25.0 | cpu | 34/731/4098/1396/0 | 25/556/2482/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261023 |
| v0.25.0 | rocm | 47/775/3828/1479/0 | 25/567/1836/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261023 |

<!-- scan-summary:end -->
