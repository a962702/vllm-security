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

_Last scanned: 2026-09-18T05:44:15Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 9/188/3308/329/0 | 9/176/3262/264/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260918 |
| nightly | cpu | 4/13/16/3/0 | 4/13/16/3/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260918 |
| nightly | rocm | 28/331/4180/509/0 | 10/211/3269/370/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260918 |
| v0.29.0 | gpu | 5/180/3350/326/0 | 5/168/3249/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260918 |
| v0.29.0 | cpu | 6/203/3827/334/0 | 6/203/3788/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260918 |
| v0.29.0 | rocm | 24/323/4203/506/0 | 6/203/3256/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260918 |
| v0.28.0 | gpu | 5/187/3535/333/0 | 5/168/3249/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260918 |
| v0.28.0 | cpu | 6/203/3883/340/0 | 6/203/3788/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260918 |
| v0.28.0 | rocm | 24/323/4231/509/0 | 6/203/3256/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260918 |
| v0.27.1 | gpu | 6/217/4002/428/0 | 6/201/3826/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260918 |
| v0.27.1 | cpu | 6/206/3895/340/0 | 6/204/3791/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260918 |
| v0.27.1 | rocm | 24/324/4254/518/0 | 6/204/3259/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260918 |
| v0.27.0 | gpu | 6/217/4002/428/0 | 6/201/3826/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260918 |
| v0.27.0 | cpu | 6/206/3895/340/0 | 6/204/3791/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260918 |
| v0.27.0 | rocm | 24/324/4254/518/0 | 6/204/3259/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260918 |
| v0.26.0 | gpu | 8/226/4027/431/0 | 6/199/3825/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260918 |
| v0.26.0 | cpu | 8/215/3939/348/0 | 6/202/3792/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260918 |
| v0.26.0 | rocm | 24/322/4254/518/0 | 6/202/3259/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260918 |
| v0.25.1 | gpu | 11/301/4634/522/0 | 6/200/3834/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260918 |
| v0.25.1 | cpu | 11/290/4550/439/0 | 6/203/3801/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260918 |
| v0.25.1 | rocm | 24/333/4331/522/0 | 6/213/3271/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260918 |
| v0.25.0 | gpu | 11/301/4634/522/0 | 6/200/3834/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260918 |
| v0.25.0 | cpu | 11/290/4550/439/0 | 6/203/3801/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260918 |
| v0.25.0 | rocm | 24/333/4331/522/0 | 6/213/3271/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260918 |
| v0.24.0 | gpu | 11/316/4701/534/0 | 6/215/3837/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260918 |
| v0.24.0 | cpu | 11/303/4577/461/0 | 6/215/3804/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260918 |
| v0.24.0 | rocm | 24/342/4364/531/0 | 6/222/3274/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260918 |
| v0.23.0 | gpu | 24/339/4752/542/0 | 6/219/3845/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260918 |
| v0.23.0 | cpu | 24/326/4628/468/0 | 6/219/3812/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260918 |
| v0.23.0 | rocm | 24/347/4388/541/0 | 6/227/3282/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260918 |
| v0.22.1 | gpu | 24/342/4762/550/0 | 6/222/3851/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260918 |
| v0.22.1 | cpu | 24/330/4635/479/0 | 6/222/3817/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260918 |
| v0.22.1 | rocm | 24/360/4523/590/0 | - | ok | - |

<!-- scan-summary:end -->
