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

_Last scanned: 2026-09-12T05:50:10Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/178/2787/326/0 | 5/166/2742/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260912 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260912 |
| nightly | rocm | 24/322/3746/506/0 | 6/202/2840/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260912 |
| v0.29.0 | gpu | 5/178/2828/326/0 | 5/166/2743/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260912 |
| v0.29.0 | cpu | 6/202/3347/334/0 | 6/202/3308/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260912 |
| v0.29.0 | rocm | 24/322/3780/506/0 | 6/202/2841/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260912 |
| v0.28.0 | gpu | 5/185/3013/333/0 | 5/166/2743/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260912 |
| v0.28.0 | cpu | 6/202/3403/340/0 | 6/202/3308/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260912 |
| v0.28.0 | rocm | 24/322/3808/509/0 | 6/202/2841/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260912 |
| v0.27.1 | gpu | 6/216/3511/428/0 | 6/200/3341/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260912 |
| v0.27.1 | cpu | 6/205/3414/340/0 | 6/203/3310/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260912 |
| v0.27.1 | rocm | 24/323/3830/518/0 | 6/203/2843/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260912 |
| v0.27.0 | gpu | 6/216/3511/428/0 | 6/200/3341/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260912 |
| v0.27.0 | cpu | 6/205/3414/340/0 | 6/203/3310/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260912 |
| v0.27.0 | rocm | 24/323/3830/518/0 | 6/203/2843/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260912 |
| v0.26.0 | gpu | 8/225/3536/431/0 | 6/198/3340/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260912 |
| v0.26.0 | cpu | 8/214/3458/348/0 | 6/201/3311/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260912 |
| v0.26.0 | rocm | 24/321/3830/518/0 | 6/201/2843/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260912 |
| v0.25.1 | gpu | 11/300/4143/522/0 | 6/199/3349/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260912 |
| v0.25.1 | cpu | 11/289/4069/439/0 | 6/202/3320/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260912 |
| v0.25.1 | rocm | 24/332/3907/522/0 | 6/212/2855/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260912 |
| v0.25.0 | gpu | 11/300/4143/522/0 | 6/199/3349/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260912 |
| v0.25.0 | cpu | 11/289/4069/439/0 | 6/202/3320/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260912 |
| v0.25.0 | rocm | 24/332/3907/522/0 | 6/212/2855/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260912 |
| v0.24.0 | gpu | 11/315/4210/534/0 | 6/214/3352/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260912 |
| v0.24.0 | cpu | 11/302/4096/461/0 | 6/214/3323/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260912 |
| v0.24.0 | rocm | 24/341/3940/531/0 | 6/221/2858/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260912 |
| v0.23.0 | gpu | 24/338/4260/542/0 | 6/218/3359/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260912 |
| v0.23.0 | cpu | 24/325/4146/468/0 | 6/218/3330/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260912 |
| v0.23.0 | rocm | 24/346/3963/541/0 | 6/226/2865/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260912 |
| v0.22.1 | gpu | 24/341/4270/550/0 | 6/221/3365/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260912 |
| v0.22.1 | cpu | 24/329/4153/479/0 | 6/221/3335/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260912 |
| v0.22.1 | rocm | 24/359/4098/590/0 | - | ok | - |

<!-- scan-summary:end -->
