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

_Last scanned: 2026-09-03T05:25:51Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/167/2670/289/0 | 5/155/2625/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260903 |
| nightly | rocm | - | - | scan_failed | - |
| v0.28.0 | gpu | 5/167/2766/293/0 | 5/155/2625/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260903 |
| v0.28.0 | cpu | 6/192/3250/315/0 | 6/192/3186/298/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260903 |
| v0.28.0 | rocm | - | - | scan_failed | - |
| v0.27.1 | gpu | 6/205/3306/403/0 | 6/189/3175/338/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260903 |
| v0.27.1 | cpu | 6/194/3259/315/0 | 6/192/3186/298/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260903 |
| v0.27.1 | rocm | - | - | scan_failed | - |
| v0.27.0 | gpu | 6/205/3306/403/0 | 6/189/3175/338/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260903 |
| v0.27.0 | cpu | 6/194/3259/315/0 | 6/192/3186/298/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260903 |
| v0.27.0 | rocm | - | - | scan_failed | - |
| v0.26.0 | gpu | 8/215/3332/406/0 | 6/188/3175/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260903 |
| v0.26.0 | cpu | 8/204/3304/323/0 | 6/191/3188/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260903 |
| v0.26.0 | rocm | - | - | scan_failed | - |
| v0.25.1 | gpu | 11/290/3934/497/0 | 6/189/3179/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260903 |
| v0.25.1 | cpu | 11/279/3910/414/0 | 6/192/3192/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260903 |
| v0.25.1 | rocm | - | - | scan_failed | - |
| v0.25.0 | gpu | 11/290/3934/497/0 | 6/189/3179/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260903 |
| v0.25.0 | cpu | 11/279/3910/414/0 | 6/192/3192/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260903 |
| v0.25.0 | rocm | - | - | scan_failed | - |
| v0.24.0 | gpu | 11/305/4001/509/0 | 6/204/3182/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260903 |
| v0.24.0 | cpu | 11/292/3937/436/0 | 6/204/3195/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260903 |
| v0.24.0 | rocm | - | - | scan_failed | - |
| v0.23.0 | gpu | 24/328/4051/517/0 | 6/208/3189/340/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260903 |
| v0.23.0 | cpu | 24/315/3987/443/0 | 6/208/3202/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260903 |
| v0.23.0 | rocm | - | - | scan_failed | - |
| v0.22.1 | gpu | 24/331/4061/525/0 | 6/211/3195/344/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260903 |
| v0.22.1 | cpu | 24/319/3995/454/0 | 6/211/3208/303/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260903 |
| v0.22.1 | rocm | - | - | scan_failed | - |
| v0.22.0 | gpu | 24/342/4066/530/0 | 6/216/3200/348/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260903 |
| v0.22.0 | cpu | 24/330/4002/459/0 | 6/216/3215/307/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260903 |
| v0.22.0 | rocm | - | - | scan_failed | - |

<!-- scan-summary:end -->
