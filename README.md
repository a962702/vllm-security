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

_Last scanned: 2026-09-17T05:53:35Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/180/3095/326/0 | 5/168/3046/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260917 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260917 |
| nightly | rocm | 24/323/4002/506/0 | 6/203/3091/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260917 |
| v0.29.0 | gpu | 5/180/3139/326/0 | 5/168/3047/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260917 |
| v0.29.0 | cpu | 6/203/3662/334/0 | 6/203/3623/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260917 |
| v0.29.0 | rocm | 24/323/4036/506/0 | 6/203/3092/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260917 |
| v0.28.0 | gpu | 5/187/3324/333/0 | 5/168/3047/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260917 |
| v0.28.0 | cpu | 6/203/3718/340/0 | 6/203/3623/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260917 |
| v0.28.0 | rocm | 24/323/4064/509/0 | 6/203/3092/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260917 |
| v0.27.1 | gpu | 6/217/3836/428/0 | 6/201/3661/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260917 |
| v0.27.1 | cpu | 6/206/3729/340/0 | 6/204/3625/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260917 |
| v0.27.1 | rocm | 24/324/4086/518/0 | 6/204/3094/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260917 |
| v0.27.0 | gpu | 6/217/3836/428/0 | 6/201/3661/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260917 |
| v0.27.0 | cpu | 6/206/3729/340/0 | 6/204/3625/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260917 |
| v0.27.0 | rocm | 24/324/4086/518/0 | 6/204/3094/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260917 |
| v0.26.0 | gpu | 8/226/3861/431/0 | 6/199/3660/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260917 |
| v0.26.0 | cpu | 8/215/3773/348/0 | 6/202/3626/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260917 |
| v0.26.0 | rocm | 24/322/4086/518/0 | 6/202/3094/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260917 |
| v0.25.1 | gpu | 11/301/4468/522/0 | 6/200/3669/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260917 |
| v0.25.1 | cpu | 11/290/4384/439/0 | 6/203/3635/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260917 |
| v0.25.1 | rocm | 24/333/4163/522/0 | 6/213/3106/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260917 |
| v0.25.0 | gpu | 11/301/4468/522/0 | 6/200/3669/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260917 |
| v0.25.0 | cpu | 11/290/4384/439/0 | 6/203/3635/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260917 |
| v0.25.0 | rocm | 24/333/4163/522/0 | 6/213/3106/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260917 |
| v0.24.0 | gpu | 11/316/4535/534/0 | 6/215/3672/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260917 |
| v0.24.0 | cpu | 11/303/4411/461/0 | 6/215/3638/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260917 |
| v0.24.0 | rocm | 24/342/4196/531/0 | 6/222/3109/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260917 |
| v0.23.0 | gpu | 24/339/4586/542/0 | 6/219/3680/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260917 |
| v0.23.0 | cpu | 24/326/4462/468/0 | 6/219/3646/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260917 |
| v0.23.0 | rocm | 24/347/4220/541/0 | 6/227/3117/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260917 |
| v0.22.1 | gpu | 24/342/4596/550/0 | 6/222/3686/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260917 |
| v0.22.1 | cpu | 24/330/4469/479/0 | 6/222/3651/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260917 |
| v0.22.1 | rocm | 24/360/4355/590/0 | - | ok | - |

<!-- scan-summary:end -->
