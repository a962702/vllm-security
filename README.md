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

_Last scanned: 2026-09-10T05:54:26Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/178/2762/326/0 | 5/166/2717/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260910 |
| nightly | rocm | 24/322/3714/507/0 | 6/202/2822/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260910 |
| v0.29.0 | gpu | 5/178/2762/326/0 | 5/166/2717/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260910 |
| v0.29.0 | cpu | 6/202/3327/334/0 | 6/202/3288/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260910 |
| v0.29.0 | rocm | 24/322/3747/507/0 | 6/202/2822/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260910 |
| v0.28.0 | gpu | 5/185/2947/333/0 | 5/166/2717/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260910 |
| v0.28.0 | cpu | 6/202/3383/340/0 | 6/202/3288/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260910 |
| v0.28.0 | rocm | 24/322/3775/510/0 | 6/202/2822/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260910 |
| v0.27.1 | gpu | 6/216/3484/428/0 | 6/200/3322/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260910 |
| v0.27.1 | cpu | 6/205/3394/340/0 | 6/203/3290/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260910 |
| v0.27.1 | rocm | 24/323/3797/519/0 | 6/203/2824/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260910 |
| v0.27.0 | gpu | 6/216/3484/428/0 | 6/200/3322/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260910 |
| v0.27.0 | cpu | 6/205/3394/340/0 | 6/203/3290/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260910 |
| v0.27.0 | rocm | 24/323/3797/519/0 | 6/203/2824/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260910 |
| v0.26.0 | gpu | 8/225/3509/431/0 | 6/198/3321/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260910 |
| v0.26.0 | cpu | 8/214/3438/348/0 | 6/201/3291/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260910 |
| v0.26.0 | rocm | 24/321/3797/519/0 | 6/201/2824/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260910 |
| v0.25.1 | gpu | 11/300/4116/522/0 | 6/199/3330/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260910 |
| v0.25.1 | cpu | 11/289/4049/439/0 | 6/202/3300/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260910 |
| v0.25.1 | rocm | 24/332/3874/523/0 | 6/212/2836/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260910 |
| v0.25.0 | gpu | 11/300/4116/522/0 | 6/199/3330/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260910 |
| v0.25.0 | cpu | 11/289/4049/439/0 | 6/202/3300/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260910 |
| v0.25.0 | rocm | 24/332/3874/523/0 | 6/212/2836/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260910 |
| v0.24.0 | gpu | 11/315/4183/534/0 | 6/214/3333/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260910 |
| v0.24.0 | cpu | 11/302/4076/461/0 | 6/214/3303/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260910 |
| v0.24.0 | rocm | 24/341/3907/532/0 | 6/221/2839/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260910 |
| v0.23.0 | gpu | 24/338/4233/542/0 | 6/218/3340/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260910 |
| v0.23.0 | cpu | 24/325/4126/468/0 | 6/218/3310/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260910 |
| v0.23.0 | rocm | 24/346/3930/542/0 | 6/226/2846/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260910 |
| v0.22.1 | gpu | 24/341/4243/550/0 | 6/221/3346/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260910 |
| v0.22.1 | cpu | 24/329/4134/479/0 | 6/221/3316/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260910 |
| v0.22.1 | rocm | 24/359/4065/591/0 | - | ok | - |

<!-- scan-summary:end -->
