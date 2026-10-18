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

_Last scanned: 2026-10-18T05:43:08Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 3/146/3038/389/0 | 3/132/3009/315/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261018 |
| nightly | cpu | 7/314/2851/796/0 | 7/314/2851/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261018 |
| nightly | rocm | 30/522/3989/1061/0 | 8/315/2196/837/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261018 |
| v0.31.0 | gpu | 10/245/3899/494/0 | 4/132/3009/315/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261018 |
| v0.31.0 | cpu | 7/316/2871/801/0 | 7/315/2851/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261018 |
| v0.31.0 | rocm | 30/522/3999/1061/0 | 8/315/2196/837/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261018 |
| v0.30.0 | gpu | 10/285/4133/533/0 | 4/132/3014/314/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261018 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261018 |
| v0.30.0 | rocm | 30/522/4045/1062/0 | 8/315/2201/838/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261018 |
| v0.29.0 | gpu | 11/292/4267/534/0 | 5/139/3031/315/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261018 |
| v0.29.0 | cpu | 12/409/3765/891/0 | 8/322/2859/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261018 |
| v0.29.0 | rocm | 31/529/4098/1063/0 | 9/322/2218/839/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261018 |
| v0.28.0 | gpu | 11/303/4441/546/0 | 5/139/3029/315/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261018 |
| v0.28.0 | cpu | 12/409/3820/897/0 | 8/322/2858/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261018 |
| v0.28.0 | rocm | 30/529/4125/1066/0 | 8/322/2217/839/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261018 |
| v0.27.1 | gpu | 13/423/3945/985/0 | 9/320/2862/835/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261018 |
| v0.27.1 | cpu | 12/412/3833/897/0 | 8/323/2862/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261018 |
| v0.27.1 | rocm | 30/530/4149/1075/0 | 8/323/2221/849/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261018 |
| v0.27.0 | gpu | 13/423/3945/985/0 | 9/320/2862/835/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261018 |
| v0.27.0 | cpu | 12/412/3833/897/0 | 8/323/2862/795/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261018 |
| v0.27.0 | rocm | 30/530/4149/1075/0 | 8/323/2221/849/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261018 |
| v0.26.0 | gpu | 15/430/3969/988/0 | 9/316/2860/836/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261018 |
| v0.26.0 | cpu | 14/419/3876/905/0 | 8/319/2862/796/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261018 |
| v0.26.0 | rocm | 30/527/4149/1075/0 | 8/320/2221/849/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261018 |
| v0.25.1 | gpu | 18/505/4577/1079/0 | 9/317/2869/836/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261018 |
| v0.25.1 | cpu | 17/494/4488/996/0 | 8/320/2871/796/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261018 |
| v0.25.1 | rocm | 30/538/4226/1079/0 | 8/331/2233/849/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261018 |
| v0.25.0 | gpu | 19/506/4578/1079/0 | 10/318/2870/836/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261018 |
| v0.25.0 | cpu | 18/495/4489/996/0 | 9/321/2872/796/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261018 |
| v0.25.0 | rocm | 31/539/4227/1079/0 | 9/332/2234/849/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261018 |
| v0.24.0 | gpu | 19/521/4645/1091/0 | 10/333/2873/836/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261018 |
| v0.24.0 | cpu | 18/508/4516/1018/0 | 9/333/2875/796/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261018 |
| v0.24.0 | rocm | 31/548/4260/1088/0 | 9/341/2237/850/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261018 |

<!-- scan-summary:end -->
