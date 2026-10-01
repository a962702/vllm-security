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

_Last scanned: 2026-10-01T07:44:36Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/181/4076/335/0 | 5/167/4047/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261001 |
| nightly | cpu | 5/205/4442/328/0 | 5/204/4437/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261001 |
| nightly | rocm | 24/330/4818/515/0 | 5/205/3854/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261001 |
| v0.30.0 | gpu | 5/184/4149/336/0 | 5/167/4048/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261001 |
| v0.30.0 | cpu | 0/7/4/0/0 | 0/7/4/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261001 |
| v0.30.0 | rocm | 24/330/4868/516/0 | 5/205/3855/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261001 |
| v0.29.0 | gpu | 6/191/4274/336/0 | 6/174/4056/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261001 |
| v0.29.0 | cpu | 7/217/4535/344/0 | 6/212/4442/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261001 |
| v0.29.0 | rocm | 25/337/4912/516/0 | 6/212/3863/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261001 |
| v0.28.0 | gpu | 6/198/4459/343/0 | 6/174/4056/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261001 |
| v0.28.0 | cpu | 7/217/4591/350/0 | 6/212/4442/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261001 |
| v0.28.0 | rocm | 25/337/4940/519/0 | 6/212/3863/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261001 |
| v0.27.1 | gpu | 7/231/4706/438/0 | 6/210/4436/361/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261001 |
| v0.27.1 | cpu | 7/220/4603/350/0 | 6/213/4445/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261001 |
| v0.27.1 | rocm | 25/338/4963/528/0 | 6/213/3866/375/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261001 |
| v0.27.0 | gpu | 7/231/4706/438/0 | 6/210/4436/361/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261001 |
| v0.27.0 | cpu | 7/220/4603/350/0 | 6/213/4445/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261001 |
| v0.27.0 | rocm | 25/338/4963/528/0 | 6/213/3866/375/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261001 |
| v0.26.0 | gpu | 9/238/4730/441/0 | 6/206/4434/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261001 |
| v0.26.0 | cpu | 9/227/4646/358/0 | 6/209/4445/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261001 |
| v0.26.0 | rocm | 25/334/4962/528/0 | 6/209/3865/375/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261001 |
| v0.25.1 | gpu | 12/313/5337/532/0 | 6/207/4443/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261001 |
| v0.25.1 | cpu | 12/302/5257/449/0 | 6/210/4454/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261001 |
| v0.25.1 | rocm | 25/345/5039/532/0 | 6/220/3877/375/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261001 |
| v0.25.0 | gpu | 13/314/5338/532/0 | 7/208/4444/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261001 |
| v0.25.0 | cpu | 13/303/5258/449/0 | 7/211/4455/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261001 |
| v0.25.0 | rocm | 26/346/5040/532/0 | 7/221/3878/375/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261001 |
| v0.24.0 | gpu | 13/329/5405/544/0 | 7/223/4447/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261001 |
| v0.24.0 | cpu | 13/316/5285/471/0 | 7/223/4458/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261001 |
| v0.24.0 | rocm | 26/355/5073/541/0 | 7/230/3881/376/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261001 |
| v0.23.0 | gpu | 26/351/5456/552/0 | 7/226/4455/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20261001 |
| v0.23.0 | cpu | 26/338/5336/478/0 | 7/226/4466/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20261001 |
| v0.23.0 | rocm | 26/359/5098/551/0 | 7/234/3890/376/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20261001 |

<!-- scan-summary:end -->
