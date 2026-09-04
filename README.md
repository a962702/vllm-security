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

_Last scanned: 2026-09-04T05:27:56Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/185/2630/326/0 | 5/173/2583/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260904 |
| nightly | rocm | - | - | scan_failed | - |
| v0.28.0 | gpu | 5/185/2726/330/0 | 5/173/2583/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260904 |
| v0.28.0 | cpu | 6/203/3219/338/0 | 6/203/3153/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260904 |
| v0.28.0 | rocm | - | - | scan_failed | - |
| v0.27.1 | gpu | 6/216/3276/426/0 | 6/200/3143/361/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260904 |
| v0.27.1 | cpu | 6/205/3228/338/0 | 6/203/3153/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260904 |
| v0.27.1 | rocm | - | - | scan_failed | - |
| v0.27.0 | gpu | 6/216/3276/426/0 | 6/200/3143/361/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260904 |
| v0.27.0 | cpu | 6/205/3228/338/0 | 6/203/3153/321/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260904 |
| v0.27.0 | rocm | - | - | scan_failed | - |
| v0.26.0 | gpu | 8/226/3302/429/0 | 6/199/3143/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260904 |
| v0.26.0 | cpu | 8/215/3273/346/0 | 6/202/3155/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260904 |
| v0.26.0 | rocm | - | - | scan_failed | - |
| v0.25.1 | gpu | 11/301/3904/520/0 | 6/200/3147/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260904 |
| v0.25.1 | cpu | 11/290/3879/437/0 | 6/203/3159/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260904 |
| v0.25.1 | rocm | - | - | scan_failed | - |
| v0.25.0 | gpu | 11/301/3904/520/0 | 6/200/3147/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260904 |
| v0.25.0 | cpu | 11/290/3879/437/0 | 6/203/3159/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260904 |
| v0.25.0 | rocm | - | - | scan_failed | - |
| v0.24.0 | gpu | 11/316/3971/532/0 | 6/215/3150/362/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260904 |
| v0.24.0 | cpu | 11/303/3906/459/0 | 6/215/3162/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260904 |
| v0.24.0 | rocm | - | - | scan_failed | - |
| v0.23.0 | gpu | 24/339/4021/540/0 | 6/219/3157/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260904 |
| v0.23.0 | cpu | 24/326/3956/466/0 | 6/219/3169/322/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260904 |
| v0.23.0 | rocm | - | - | scan_failed | - |
| v0.22.1 | gpu | 24/342/4031/548/0 | 6/222/3163/367/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260904 |
| v0.22.1 | cpu | 24/330/3964/477/0 | 6/222/3175/326/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260904 |
| v0.22.1 | rocm | - | - | scan_failed | - |
| v0.22.0 | gpu | 24/353/4036/553/0 | 6/227/3168/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260904 |
| v0.22.0 | cpu | 24/341/3971/482/0 | 6/227/3182/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260904 |
| v0.22.0 | rocm | - | - | scan_failed | - |

<!-- scan-summary:end -->
