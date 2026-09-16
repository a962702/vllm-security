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

_Last scanned: 2026-09-16T05:47:30Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/180/2792/326/0 | 5/168/2744/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260916 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260916 |
| nightly | rocm | 24/323/3750/506/0 | 6/203/2839/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260916 |
| v0.29.0 | gpu | 5/180/2833/326/0 | 5/168/2745/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260916 |
| v0.29.0 | cpu | 6/203/3411/334/0 | 6/203/3372/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260916 |
| v0.29.0 | rocm | 24/323/3784/506/0 | 6/203/2840/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260916 |
| v0.28.0 | gpu | 5/187/3018/333/0 | 5/168/2745/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260916 |
| v0.28.0 | cpu | 6/203/3467/340/0 | 6/203/3372/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260916 |
| v0.28.0 | rocm | 24/323/3812/509/0 | 6/203/2840/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260916 |
| v0.27.1 | gpu | 6/217/3580/428/0 | 6/201/3405/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260916 |
| v0.27.1 | cpu | 6/206/3478/340/0 | 6/204/3374/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260916 |
| v0.27.1 | rocm | 24/324/3834/518/0 | 6/204/2842/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260916 |
| v0.27.0 | gpu | 6/217/3580/428/0 | 6/201/3405/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260916 |
| v0.27.0 | cpu | 6/206/3478/340/0 | 6/204/3374/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260916 |
| v0.27.0 | rocm | 24/324/3834/518/0 | 6/204/2842/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260916 |
| v0.26.0 | gpu | 8/226/3605/431/0 | 6/199/3404/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260916 |
| v0.26.0 | cpu | 8/215/3522/348/0 | 6/202/3375/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260916 |
| v0.26.0 | rocm | 24/322/3834/518/0 | 6/202/2842/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260916 |
| v0.25.1 | gpu | 11/301/4212/522/0 | 6/200/3413/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260916 |
| v0.25.1 | cpu | 11/290/4133/439/0 | 6/203/3384/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260916 |
| v0.25.1 | rocm | 24/333/3911/522/0 | 6/213/2854/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260916 |
| v0.25.0 | gpu | 11/301/4212/522/0 | 6/200/3413/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260916 |
| v0.25.0 | cpu | 11/290/4133/439/0 | 6/203/3384/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260916 |
| v0.25.0 | rocm | 24/333/3911/522/0 | 6/213/2854/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260916 |
| v0.24.0 | gpu | 11/316/4279/534/0 | 6/215/3416/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260916 |
| v0.24.0 | cpu | 11/303/4160/461/0 | 6/215/3387/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260916 |
| v0.24.0 | rocm | 24/342/3944/531/0 | 6/222/2857/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260916 |
| v0.23.0 | gpu | 24/339/4329/542/0 | 6/219/3423/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260916 |
| v0.23.0 | cpu | 24/326/4210/468/0 | 6/219/3394/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260916 |
| v0.23.0 | rocm | 24/347/3967/541/0 | 6/227/2864/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260916 |
| v0.22.1 | gpu | 24/342/4339/550/0 | 6/222/3429/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260916 |
| v0.22.1 | cpu | 24/330/4217/479/0 | 6/222/3399/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260916 |
| v0.22.1 | rocm | 24/360/4102/590/0 | - | ok | - |

<!-- scan-summary:end -->
