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

_Last scanned: 2026-09-11T05:55:14Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/178/2810/326/0 | 5/166/2725/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20260911 |
| nightly | cpu | 0/5/2/0/0 | 0/5/2/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20260911 |
| nightly | rocm | 24/322/3733/507/0 | 6/202/2827/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20260911 |
| v0.29.0 | gpu | 5/178/2811/326/0 | 5/166/2726/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20260911 |
| v0.29.0 | cpu | 6/202/3333/334/0 | 6/202/3294/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20260911 |
| v0.29.0 | rocm | 24/322/3767/507/0 | 6/202/2828/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20260911 |
| v0.28.0 | gpu | 5/185/2996/333/0 | 5/166/2726/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20260911 |
| v0.28.0 | cpu | 6/202/3389/340/0 | 6/202/3294/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20260911 |
| v0.28.0 | rocm | 24/322/3795/510/0 | 6/202/2828/368/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20260911 |
| v0.27.1 | gpu | 6/216/3498/428/0 | 6/200/3328/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20260911 |
| v0.27.1 | cpu | 6/205/3400/340/0 | 6/203/3296/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20260911 |
| v0.27.1 | rocm | 24/323/3817/519/0 | 6/203/2830/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20260911 |
| v0.27.0 | gpu | 6/216/3498/428/0 | 6/200/3328/363/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20260911 |
| v0.27.0 | cpu | 6/205/3400/340/0 | 6/203/3296/323/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20260911 |
| v0.27.0 | rocm | 24/323/3817/519/0 | 6/203/2830/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20260911 |
| v0.26.0 | gpu | 8/225/3523/431/0 | 6/198/3327/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20260911 |
| v0.26.0 | cpu | 8/214/3444/348/0 | 6/201/3297/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20260911 |
| v0.26.0 | rocm | 24/321/3817/519/0 | 6/201/2830/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20260911 |
| v0.25.1 | gpu | 11/300/4130/522/0 | 6/199/3336/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20260911 |
| v0.25.1 | cpu | 11/289/4055/439/0 | 6/202/3306/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20260911 |
| v0.25.1 | rocm | 24/332/3894/523/0 | 6/212/2842/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20260911 |
| v0.25.0 | gpu | 11/300/4130/522/0 | 6/199/3336/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20260911 |
| v0.25.0 | cpu | 11/289/4055/439/0 | 6/202/3306/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20260911 |
| v0.25.0 | rocm | 24/332/3894/523/0 | 6/212/2842/378/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20260911 |
| v0.24.0 | gpu | 11/315/4197/534/0 | 6/214/3339/364/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20260911 |
| v0.24.0 | cpu | 11/302/4082/461/0 | 6/214/3309/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20260911 |
| v0.24.0 | rocm | 24/341/3927/532/0 | 6/221/2845/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20260911 |
| v0.23.0 | gpu | 24/338/4247/542/0 | 6/218/3346/365/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20260911 |
| v0.23.0 | cpu | 24/325/4132/468/0 | 6/218/3316/324/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20260911 |
| v0.23.0 | rocm | 24/346/3950/542/0 | 6/226/2852/379/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20260911 |
| v0.22.1 | gpu | 24/341/4257/550/0 | 6/221/3352/369/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.22.1-20260911 |
| v0.22.1 | cpu | 24/329/4140/479/0 | 6/221/3322/328/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.22.1-20260911 |
| v0.22.1 | rocm | 24/359/4085/591/0 | - | ok | - |

<!-- scan-summary:end -->
