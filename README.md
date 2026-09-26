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

_Last scanned: 2026-09-26T06:08:20Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/176/3607/325/0 | 5/164/3578/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260926 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260926 |
| nightly | rocm | - | - | scan_failed | - |
| v0.30.0 | gpu | 5/179/3663/326/0 | 5/164/3578/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20260926 |
| v0.30.0 | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20260926 |
| v0.30.0 | rocm | 24/323/4485/506/0 | 6/203/3503/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20260926 |
| v0.29.0 | gpu | 5/179/3781/326/0 | 5/164/3579/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260926 |
| v0.29.0 | cpu | 6/203/4137/334/0 | 6/203/4067/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260926 |
| v0.29.0 | rocm | 24/323/4522/506/0 | 6/203/3504/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260926 |
| v0.28.0 | gpu | 5/186/3966/333/0 | 5/164/3579/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260926 |
| v0.28.0 | cpu | 6/203/4193/340/0 | 6/203/4067/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260926 |
| v0.28.0 | rocm | 24/323/4550/509/0 | 6/203/3504/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260926 |
| v0.27.1 | gpu | 6/217/4309/428/0 | 6/201/4064/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260926 |
| v0.27.1 | cpu | 6/206/4205/340/0 | 6/204/4070/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260926 |
| v0.27.1 | rocm | 24/324/4573/518/0 | 6/204/3507/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260926 |
| v0.27.0 | gpu | 6/217/4309/428/0 | 6/201/4064/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260926 |
| v0.27.0 | cpu | 6/206/4205/340/0 | 6/204/4070/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260926 |
| v0.27.0 | rocm | 24/324/4573/518/0 | 6/204/3507/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260926 |
| v0.26.0 | gpu | 8/226/4334/431/0 | 6/199/4063/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260926 |
| v0.26.0 | cpu | 8/215/4249/348/0 | 6/202/4071/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260926 |
| v0.26.0 | rocm | 24/322/4573/518/0 | 6/202/3507/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260926 |
| v0.25.1 | gpu | 11/301/4941/522/0 | 6/200/4072/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260926 |
| v0.25.1 | cpu | 11/290/4860/439/0 | 6/203/4080/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260926 |
| v0.25.1 | rocm | 24/333/4650/522/0 | 6/213/3519/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260926 |
| v0.25.0 | gpu | 12/302/4942/522/0 | 7/201/4073/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260926 |
| v0.25.0 | cpu | 12/291/4861/439/0 | 7/204/4081/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260926 |
| v0.25.0 | rocm | 25/334/4651/522/0 | 7/214/3520/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260926 |
| v0.24.0 | gpu | 12/317/5009/534/0 | 7/216/4076/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260926 |
| v0.24.0 | cpu | 12/304/4888/461/0 | 7/216/4084/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260926 |
| v0.24.0 | rocm | 25/343/4684/531/0 | 7/223/3523/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260926 |
| v0.23.0 | gpu | 25/339/5060/542/0 | 7/219/4084/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260926 |
| v0.23.0 | cpu | 25/326/4939/468/0 | 7/219/4092/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260926 |
| v0.23.0 | rocm | 25/347/4709/541/0 | 7/227/3532/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260926 |

<!-- scan-summary:end -->
