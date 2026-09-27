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

_Last scanned: 2026-09-27T07:46:08Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/176/3592/325/0 | 5/164/3563/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260927 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260927 |
| nightly | rocm | - | - | scan_failed | - |
| v0.30.0 | gpu | 5/179/3660/326/0 | 5/164/3563/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20260927 |
| v0.30.0 | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20260927 |
| v0.30.0 | rocm | 24/323/4482/506/0 | 6/203/3491/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20260927 |
| v0.29.0 | gpu | 5/179/3778/326/0 | 5/164/3564/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260927 |
| v0.29.0 | cpu | 6/203/4134/334/0 | 6/203/4055/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260927 |
| v0.29.0 | rocm | 24/323/4519/506/0 | 6/203/3492/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260927 |
| v0.28.0 | gpu | 5/186/3963/333/0 | 5/164/3564/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260927 |
| v0.28.0 | cpu | 6/203/4190/340/0 | 6/203/4055/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260927 |
| v0.28.0 | rocm | 24/323/4547/509/0 | 6/203/3492/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260927 |
| v0.27.1 | gpu | 6/217/4306/428/0 | 6/201/4052/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260927 |
| v0.27.1 | cpu | 6/206/4202/340/0 | 6/204/4058/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260927 |
| v0.27.1 | rocm | 24/324/4570/518/0 | 6/204/3495/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260927 |
| v0.27.0 | gpu | 6/217/4306/428/0 | 6/201/4052/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260927 |
| v0.27.0 | cpu | 6/206/4202/340/0 | 6/204/4058/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260927 |
| v0.27.0 | rocm | 24/324/4570/518/0 | 6/204/3495/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260927 |
| v0.26.0 | gpu | 8/226/4331/431/0 | 6/199/4051/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260927 |
| v0.26.0 | cpu | 8/215/4246/348/0 | 6/202/4059/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260927 |
| v0.26.0 | rocm | 24/322/4570/518/0 | 6/202/3495/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260927 |
| v0.25.1 | gpu | 11/301/4938/522/0 | 6/200/4060/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260927 |
| v0.25.1 | cpu | 11/290/4857/439/0 | 6/203/4068/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260927 |
| v0.25.1 | rocm | 24/333/4647/522/0 | 6/213/3507/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260927 |
| v0.25.0 | gpu | 12/302/4939/522/0 | 7/201/4061/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260927 |
| v0.25.0 | cpu | 12/291/4858/439/0 | 7/204/4069/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260927 |
| v0.25.0 | rocm | 25/334/4648/522/0 | 7/214/3508/377/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260927 |
| v0.24.0 | gpu | 12/317/5006/534/0 | 7/216/4064/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260927 |
| v0.24.0 | cpu | 12/304/4885/461/0 | 7/216/4072/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260927 |
| v0.24.0 | rocm | 25/343/4681/531/0 | 7/223/3511/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260927 |
| v0.23.0 | gpu | 25/339/5057/542/0 | 7/219/4072/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260927 |
| v0.23.0 | cpu | 25/326/4936/468/0 | 7/219/4080/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260927 |
| v0.23.0 | rocm | 25/347/4706/541/0 | 7/227/3520/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260927 |

<!-- scan-summary:end -->
