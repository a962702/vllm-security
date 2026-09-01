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

_Last scanned: 2026-09-01T04:39:48Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/167/2643/291/0 | 5/155/2538/239/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260901 |
| nightly | rocm | - | - | scan_failed | - |
| v0.28.0 | gpu | 5/167/2679/291/0 | 5/155/2538/239/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260901 |
| v0.28.0 | cpu | 6/192/3182/314/0 | 6/192/3118/304/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260901 |
| v0.28.0 | rocm | - | - | scan_failed | - |
| v0.27.1 | gpu | 6/205/3238/401/0 | 6/189/3107/344/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260901 |
| v0.27.1 | cpu | 6/194/3191/314/0 | 6/192/3118/304/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260901 |
| v0.27.1 | rocm | - | - | scan_failed | - |
| v0.27.0 | gpu | 6/205/3238/401/0 | 6/189/3107/344/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260901 |
| v0.27.0 | cpu | 6/194/3191/314/0 | 6/192/3118/304/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260901 |
| v0.27.0 | rocm | - | - | scan_failed | - |
| v0.26.0 | gpu | 8/215/3263/404/0 | 6/188/3106/345/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260901 |
| v0.26.0 | cpu | 8/204/3233/322/0 | 6/191/3117/305/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260901 |
| v0.26.0 | rocm | - | - | scan_failed | - |
| v0.25.1 | gpu | 11/290/3865/495/0 | 6/189/3110/345/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260901 |
| v0.25.1 | cpu | 11/279/3839/413/0 | 6/192/3121/305/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260901 |
| v0.25.1 | rocm | - | - | scan_failed | - |
| v0.25.0 | gpu | 11/290/3865/495/0 | 6/189/3110/345/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260901 |
| v0.25.0 | cpu | 11/279/3839/413/0 | 6/192/3121/305/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260901 |
| v0.25.0 | rocm | - | - | scan_failed | - |
| v0.24.0 | gpu | 11/305/3932/507/0 | 6/204/3113/345/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260901 |
| v0.24.0 | cpu | 11/292/3866/435/0 | 6/204/3124/305/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260901 |
| v0.24.0 | rocm | - | - | scan_failed | - |
| v0.23.0 | gpu | 24/328/3982/515/0 | 6/208/3120/346/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260901 |
| v0.23.0 | cpu | 24/315/3916/442/0 | 6/208/3131/305/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260901 |
| v0.23.0 | rocm | - | - | scan_failed | - |
| v0.22.1 | gpu | 24/331/3992/523/0 | 6/211/3126/350/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260901 |
| v0.22.1 | cpu | 24/319/3924/453/0 | 6/211/3137/309/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260901 |
| v0.22.1 | rocm | - | - | scan_failed | - |
| v0.22.0 | gpu | 24/341/3997/528/0 | 6/215/3131/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260901 |
| v0.22.0 | cpu | 24/329/3931/458/0 | 6/215/3144/313/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260901 |
| v0.22.0 | rocm | - | - | scan_failed | - |

<!-- scan-summary:end -->
