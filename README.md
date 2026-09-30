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

_Last scanned: 2026-09-30T06:47:22Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/176/3593/325/0 | 5/164/3564/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260930 |
| nightly | cpu | 6/203/4065/325/0 | 6/203/4060/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260930 |
| nightly | rocm | 24/323/4427/505/0 | 6/203/3477/366/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260930 |
| v0.30.0 | gpu | 5/179/3665/326/0 | 5/164/3564/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20260930 |
| v0.30.0 | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20260930 |
| v0.30.0 | rocm | 24/323/4476/506/0 | 6/203/3477/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20260930 |
| v0.29.0 | gpu | 6/184/3787/326/0 | 6/169/3569/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260930 |
| v0.29.0 | cpu | 7/208/4140/334/0 | 7/208/4061/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260930 |
| v0.29.0 | rocm | 25/328/4517/506/0 | 7/208/3482/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260930 |
| v0.28.0 | gpu | 6/191/3972/333/0 | 6/169/3569/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260930 |
| v0.28.0 | cpu | 7/208/4196/340/0 | 7/208/4061/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260930 |
| v0.28.0 | rocm | 25/328/4545/509/0 | 7/208/3482/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260930 |
| v0.27.1 | gpu | 7/222/4311/428/0 | 7/206/4055/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260930 |
| v0.27.1 | cpu | 7/211/4208/340/0 | 7/209/4064/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260930 |
| v0.27.1 | rocm | 25/329/4568/518/0 | 7/209/3485/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260930 |
| v0.27.0 | gpu | 7/222/4311/428/0 | 7/206/4055/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260930 |
| v0.27.0 | cpu | 7/211/4208/340/0 | 7/209/4064/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260930 |
| v0.27.0 | rocm | 25/329/4568/518/0 | 7/209/3485/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260930 |
| v0.26.0 | gpu | 9/231/4336/431/0 | 7/204/4054/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260930 |
| v0.26.0 | cpu | 9/220/4252/348/0 | 7/207/4065/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260930 |
| v0.26.0 | rocm | 25/327/4568/518/0 | 7/207/3485/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260930 |
| v0.25.1 | gpu | 12/306/4943/522/0 | 7/205/4063/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260930 |
| v0.25.1 | cpu | 12/295/4863/439/0 | 7/208/4074/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260930 |
| v0.25.1 | rocm | 25/338/4645/522/0 | 7/218/3497/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260930 |
| v0.25.0 | gpu | 13/307/4944/522/0 | 8/206/4064/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260930 |
| v0.25.0 | cpu | 13/296/4864/439/0 | 8/209/4075/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260930 |
| v0.25.0 | rocm | 26/339/4646/522/0 | 8/219/3498/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260930 |
| v0.24.0 | gpu | 13/322/5011/534/0 | 8/221/4067/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260930 |
| v0.24.0 | cpu | 13/309/4891/461/0 | 8/221/4078/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260930 |
| v0.24.0 | rocm | 26/348/4679/531/0 | 8/228/3501/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260930 |
| v0.23.0 | gpu | 26/344/5062/542/0 | 8/224/4075/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260930 |
| v0.23.0 | cpu | 26/331/4942/468/0 | 8/224/4086/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260930 |
| v0.23.0 | rocm | 26/352/4704/541/0 | 8/232/3510/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260930 |

<!-- scan-summary:end -->
