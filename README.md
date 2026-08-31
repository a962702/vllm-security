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

_Last scanned: 2026-08-31T05:02:38Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/167/2411/286/0 | 5/155/2368/237/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260831 |
| nightly | rocm | 24/312/3298/472/0 | 6/192/2471/344/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260831 |
| v0.28.0 | gpu | 5/167/2447/286/0 | 5/155/2368/237/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260831 |
| v0.28.0 | cpu | 6/192/3006/308/0 | 6/192/2984/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260831 |
| v0.28.0 | rocm | 24/312/3326/475/0 | 6/192/2471/344/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260831 |
| v0.27.1 | gpu | 6/205/3062/395/0 | 6/189/2973/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260831 |
| v0.27.1 | cpu | 6/194/3015/308/0 | 6/192/2984/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260831 |
| v0.27.1 | rocm | 24/312/3346/484/0 | 6/192/2471/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260831 |
| v0.27.0 | gpu | 6/205/3062/395/0 | 6/189/2973/339/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260831 |
| v0.27.0 | cpu | 6/194/3015/308/0 | 6/192/2984/299/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260831 |
| v0.27.0 | rocm | 24/312/3346/484/0 | 6/192/2471/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260831 |
| v0.26.0 | gpu | 8/215/3087/398/0 | 6/188/2972/340/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260831 |
| v0.26.0 | cpu | 8/204/3057/316/0 | 6/191/2983/300/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260831 |
| v0.26.0 | rocm | 24/311/3346/484/0 | 6/191/2471/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260831 |
| v0.25.1 | gpu | 11/290/3689/489/0 | 6/189/2976/340/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260831 |
| v0.25.1 | cpu | 11/279/3663/407/0 | 6/192/2987/300/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260831 |
| v0.25.1 | rocm | 24/322/3418/488/0 | 6/202/2478/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260831 |
| v0.25.0 | gpu | 11/290/3689/489/0 | 6/189/2976/340/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260831 |
| v0.25.0 | cpu | 11/279/3663/407/0 | 6/192/2987/300/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260831 |
| v0.25.0 | rocm | 24/322/3418/488/0 | 6/202/2478/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260831 |
| v0.24.0 | gpu | 11/305/3756/501/0 | 6/204/2979/340/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260831 |
| v0.24.0 | cpu | 11/292/3690/429/0 | 6/204/2990/300/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260831 |
| v0.24.0 | rocm | 24/331/3451/497/0 | 6/211/2481/355/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260831 |
| v0.23.0 | gpu | 24/328/3806/509/0 | 6/208/2986/341/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260831 |
| v0.23.0 | cpu | 24/315/3740/436/0 | 6/208/2997/300/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260831 |
| v0.23.0 | rocm | 24/336/3474/507/0 | 6/216/2488/355/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260831 |
| v0.22.1 | gpu | 24/331/3816/517/0 | 6/211/2992/345/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260831 |
| v0.22.1 | cpu | 24/319/3748/447/0 | 6/211/3003/304/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260831 |
| v0.22.1 | rocm | - | - | scan_failed | - |
| v0.22.0 | gpu | 24/341/3821/522/0 | 6/215/2997/349/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.0-20260831 |
| v0.22.0 | cpu | 24/329/3755/452/0 | 6/215/3010/308/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.0-20260831 |
| v0.22.0 | rocm | 24/353/3590/560/0 | - | ok | - |

<!-- scan-summary:end -->
