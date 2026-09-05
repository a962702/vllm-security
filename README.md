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

_Last scanned: 2026-09-05T05:20:53Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/185/2707/329/0 | 5/173/2662/264/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260905 |
| nightly | rocm | - | - | scan_failed | - |
| v0.28.0 | gpu | 5/185/2805/333/0 | 5/173/2662/264/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260905 |
| v0.28.0 | cpu | 6/203/3249/340/0 | 6/203/3183/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260905 |
| v0.28.0 | rocm | - | - | scan_failed | - |
| v0.27.1 | gpu | 6/216/3347/428/0 | 6/200/3214/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260905 |
| v0.27.1 | cpu | 6/205/3258/340/0 | 6/203/3183/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260905 |
| v0.27.1 | rocm | - | - | scan_failed | - |
| v0.27.0 | gpu | 6/216/3347/428/0 | 6/200/3214/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260905 |
| v0.27.0 | cpu | 6/205/3258/340/0 | 6/203/3183/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260905 |
| v0.27.0 | rocm | - | - | scan_failed | - |
| v0.26.0 | gpu | 8/226/3373/431/0 | 6/199/3214/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260905 |
| v0.26.0 | cpu | 8/215/3303/348/0 | 6/202/3185/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260905 |
| v0.26.0 | rocm | - | - | scan_failed | - |
| v0.25.1 | gpu | 11/301/3979/522/0 | 6/200/3222/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260905 |
| v0.25.1 | cpu | 11/290/3913/439/0 | 6/203/3193/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260905 |
| v0.25.1 | rocm | - | - | scan_failed | - |
| v0.25.0 | gpu | 11/301/3979/522/0 | 6/200/3222/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260905 |
| v0.25.0 | cpu | 11/290/3913/439/0 | 6/203/3193/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260905 |
| v0.25.0 | rocm | - | - | scan_failed | - |
| v0.24.0 | gpu | 11/316/4046/534/0 | 6/215/3225/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260905 |
| v0.24.0 | cpu | 11/303/3940/461/0 | 6/215/3196/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260905 |
| v0.24.0 | rocm | - | - | scan_failed | - |
| v0.23.0 | gpu | 24/339/4096/542/0 | 6/219/3232/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260905 |
| v0.23.0 | cpu | 24/326/3990/468/0 | 6/219/3203/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260905 |
| v0.23.0 | rocm | - | - | scan_failed | - |
| v0.22.1 | gpu | 24/342/4106/550/0 | 6/222/3238/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260905 |
| v0.22.1 | cpu | 24/330/3998/479/0 | 6/222/3209/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260905 |
| v0.22.1 | rocm | - | - | scan_failed | - |
| v0.22.0 | gpu | 24/353/4111/555/0 | 6/227/3243/373/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260905 |
| v0.22.0 | cpu | 24/341/4005/484/0 | 6/227/3216/332/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260905 |
| v0.22.0 | rocm | - | - | scan_failed | - |

<!-- scan-summary:end -->
