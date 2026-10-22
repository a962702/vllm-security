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

_Last scanned: 2026-10-22T05:57:46Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 14/390/2620/827/0 | 14/376/2591/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261022 |
| nightly | cpu | 19/522/2446/1170/0 | 19/522/2446/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261022 |
| nightly | rocm | 23/539/1799/1213/0 | 23/539/1799/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261022 |
| v0.32.0 | gpu | 17/390/2620/827/0 | 17/376/2591/753/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261022 |
| v0.32.0 | cpu | 20/522/2446/1170/0 | 20/522/2446/1169/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261022 |
| v0.32.0 | rocm | 46/747/3594/1443/0 | 24/539/1800/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261022 |
| v0.31.0 | gpu | 28/515/3476/970/0 | 21/395/2603/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261022 |
| v0.31.0 | cpu | 23/543/2478/1201/0 | 23/542/2458/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261022 |
| v0.31.0 | rocm | 46/750/3605/1461/0 | 24/542/1803/1213/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261022 |
| v0.30.0 | gpu | 28/555/3710/1009/0 | 21/395/2608/754/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261022 |
| v0.30.0 | cpu | 5/26/19/2/0 | 5/26/19/2/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261022 |
| v0.30.0 | rocm | 46/750/3651/1462/0 | 24/542/1808/1214/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261022 |
| v0.29.0 | gpu | 29/562/3844/1010/0 | 22/402/2625/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261022 |
| v0.29.0 | cpu | 28/637/3371/1291/0 | 24/549/2466/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261022 |
| v0.29.0 | rocm | 47/757/3704/1463/0 | 25/549/1825/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261022 |
| v0.28.0 | gpu | 29/573/4018/1022/0 | 22/402/2623/755/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261022 |
| v0.28.0 | cpu | 28/637/3426/1297/0 | 24/549/2465/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261022 |
| v0.28.0 | rocm | 46/757/3731/1466/0 | 24/549/1824/1215/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261022 |
| v0.27.1 | gpu | 30/651/3551/1385/0 | 26/547/2469/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261022 |
| v0.27.1 | cpu | 28/640/3439/1297/0 | 24/550/2469/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261022 |
| v0.27.1 | rocm | 46/758/3755/1475/0 | 24/550/1828/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261022 |
| v0.27.0 | gpu | 30/651/3551/1385/0 | 26/547/2469/1211/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261022 |
| v0.27.0 | cpu | 28/640/3439/1297/0 | 24/550/2469/1171/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261022 |
| v0.27.0 | rocm | 46/758/3755/1475/0 | 24/550/1828/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261022 |
| v0.26.0 | gpu | 31/658/3575/1388/0 | 25/543/2467/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261022 |
| v0.26.0 | cpu | 29/647/3482/1305/0 | 23/546/2469/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261022 |
| v0.26.0 | rocm | 45/755/3755/1475/0 | 23/547/1828/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261022 |
| v0.25.1 | gpu | 34/733/4183/1479/0 | 25/544/2476/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261022 |
| v0.25.1 | cpu | 32/722/4094/1396/0 | 23/547/2478/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261022 |
| v0.25.1 | rocm | 45/766/3832/1479/0 | 23/558/1840/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261022 |
| v0.25.0 | gpu | 35/734/4184/1479/0 | 26/545/2477/1212/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261022 |
| v0.25.0 | cpu | 33/723/4095/1396/0 | 24/548/2479/1172/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261022 |
| v0.25.0 | rocm | 46/767/3833/1479/0 | 24/559/1841/1225/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261022 |

<!-- scan-summary:end -->
