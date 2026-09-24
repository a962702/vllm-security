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

_Last scanned: 2026-09-24T05:58:08Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/180/3641/326/0 | 5/168/3612/262/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260924 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260924 |
| nightly | rocm | - | - | scan_failed | - |
| v0.30.0 | gpu | 5/180/3659/326/0 | 5/168/3612/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20260924 |
| v0.30.0 | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20260924 |
| v0.30.0 | rocm | 24/323/4467/506/0 | 6/203/3507/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20260924 |
| v0.29.0 | gpu | 5/180/3777/326/0 | 5/168/3613/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260924 |
| v0.29.0 | cpu | 6/203/4131/334/0 | 6/203/4072/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260924 |
| v0.29.0 | rocm | 24/323/4504/506/0 | 6/203/3508/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260924 |
| v0.28.0 | gpu | 5/187/3962/333/0 | 5/168/3613/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260924 |
| v0.28.0 | cpu | 6/203/4187/340/0 | 6/203/4072/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260924 |
| v0.28.0 | rocm | 24/323/4532/509/0 | 6/203/3508/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260924 |
| v0.27.1 | gpu | 6/217/4303/428/0 | 6/201/4080/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260924 |
| v0.27.1 | cpu | 6/206/4199/340/0 | 6/204/4075/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260924 |
| v0.27.1 | rocm | 24/324/4555/518/0 | 6/204/3511/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260924 |
| v0.27.0 | gpu | 6/217/4303/428/0 | 6/201/4080/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260924 |
| v0.27.0 | cpu | 6/206/4199/340/0 | 6/204/4075/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260924 |
| v0.27.0 | rocm | 24/324/4555/518/0 | 6/204/3511/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260924 |
| v0.26.0 | gpu | 8/226/4328/431/0 | 6/199/4079/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260924 |
| v0.26.0 | cpu | 8/215/4243/348/0 | 6/202/4076/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260924 |
| v0.26.0 | rocm | 24/322/4555/518/0 | 6/202/3511/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260924 |
| v0.25.1 | gpu | 11/301/4935/522/0 | 6/200/4088/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260924 |
| v0.25.1 | cpu | 11/290/4854/439/0 | 6/203/4085/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260924 |
| v0.25.1 | rocm | 24/333/4632/522/0 | 6/213/3523/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260924 |
| v0.25.0 | gpu | 12/302/4936/522/0 | 7/201/4089/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260924 |
| v0.25.0 | cpu | 12/291/4855/439/0 | 7/204/4086/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260924 |
| v0.25.0 | rocm | 25/334/4633/522/0 | 7/214/3524/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260924 |
| v0.24.0 | gpu | 12/317/5003/534/0 | 7/216/4092/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260924 |
| v0.24.0 | cpu | 12/304/4882/461/0 | 7/216/4089/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260924 |
| v0.24.0 | rocm | 25/343/4666/531/0 | 7/223/3527/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260924 |
| v0.23.0 | gpu | 25/339/5054/542/0 | 7/219/4100/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260924 |
| v0.23.0 | cpu | 25/326/4933/468/0 | 7/219/4097/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260924 |
| v0.23.0 | rocm | 25/347/4690/541/0 | 7/227/3535/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260924 |

<!-- scan-summary:end -->
