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

_Last scanned: 2026-09-08T05:47:21Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/178/2753/326/0 | 5/166/2708/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260908 |
| nightly | rocm | 24/323/3685/507/0 | 6/203/2821/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260908 |
| v0.28.0 | gpu | 5/185/2938/333/0 | 5/166/2708/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260908 |
| v0.28.0 | cpu | 6/203/3355/340/0 | 6/203/3288/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260908 |
| v0.28.0 | rocm | 24/323/3746/510/0 | 6/203/2821/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260908 |
| v0.27.1 | gpu | 6/216/3453/428/0 | 6/200/3319/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260908 |
| v0.27.1 | cpu | 6/205/3364/340/0 | 6/203/3288/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260908 |
| v0.27.1 | rocm | 24/323/3766/519/0 | 6/203/2821/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260908 |
| v0.27.0 | gpu | 6/216/3453/428/0 | 6/200/3319/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260908 |
| v0.27.0 | cpu | 6/205/3364/340/0 | 6/203/3288/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260908 |
| v0.27.0 | rocm | 24/323/3766/519/0 | 6/203/2821/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260908 |
| v0.26.0 | gpu | 8/226/3479/431/0 | 6/199/3319/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260908 |
| v0.26.0 | cpu | 8/215/3409/348/0 | 6/202/3290/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260908 |
| v0.26.0 | rocm | 24/322/3767/519/0 | 6/202/2822/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260908 |
| v0.25.1 | gpu | 11/301/4085/522/0 | 6/200/3327/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260908 |
| v0.25.1 | cpu | 11/290/4019/439/0 | 6/203/3298/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260908 |
| v0.25.1 | rocm | 24/333/3843/523/0 | 6/213/2833/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260908 |
| v0.25.0 | gpu | 11/301/4085/522/0 | 6/200/3327/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260908 |
| v0.25.0 | cpu | 11/290/4019/439/0 | 6/203/3298/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260908 |
| v0.25.0 | rocm | 24/333/3843/523/0 | 6/213/2833/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260908 |
| v0.24.0 | gpu | 11/316/4152/534/0 | 6/215/3330/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260908 |
| v0.24.0 | cpu | 11/303/4046/461/0 | 6/215/3301/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260908 |
| v0.24.0 | rocm | 24/342/3876/532/0 | 6/222/2836/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260908 |
| v0.23.0 | gpu | 24/339/4202/542/0 | 6/219/3337/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260908 |
| v0.23.0 | cpu | 24/326/4096/468/0 | 6/219/3308/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260908 |
| v0.23.0 | rocm | 24/347/3899/542/0 | 6/227/2843/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260908 |
| v0.22.1 | gpu | 24/342/4212/550/0 | 6/222/3343/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260908 |
| v0.22.1 | cpu | 24/330/4104/479/0 | 6/222/3314/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260908 |
| v0.22.1 | rocm | 24/360/4014/591/0 | - | ok | - |
| v0.22.0 | gpu | 24/353/4217/555/0 | 6/227/3348/373/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260908 |
| v0.22.0 | cpu | 24/341/4111/484/0 | 6/227/3321/332/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260908 |
| v0.22.0 | rocm | 24/365/4019/595/0 | - | ok | - |

<!-- scan-summary:end -->
