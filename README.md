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

_Last scanned: 2026-10-09T07:22:18Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/155/4042/320/0 | 5/141/4013/246/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261009 |
| nightly | cpu | 3/176/3411/444/0 | 3/175/3411/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261009 |
| nightly | rocm | 25/383/4588/703/0 | 3/176/2828/480/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261009 |
| v0.31.0 | gpu | 5/155/4046/320/0 | 5/141/4013/246/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261009 |
| v0.31.0 | cpu | 3/177/3414/444/0 | 3/176/3411/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261009 |
| v0.31.0 | rocm | 25/383/4596/703/0 | 3/176/2828/480/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261009 |
| v0.30.0 | gpu | 5/193/4286/355/0 | 5/141/4018/245/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261009 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261009 |
| v0.30.0 | rocm | 25/383/4642/704/0 | 3/176/2833/481/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261009 |
| v0.29.0 | gpu | 6/200/4420/356/0 | 6/148/4035/246/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261009 |
| v0.29.0 | cpu | 8/270/4313/533/0 | 4/183/3423/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261009 |
| v0.29.0 | rocm | 26/390/4695/705/0 | 4/183/2850/482/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261009 |
| v0.28.0 | gpu | 6/207/4602/363/0 | 6/148/4032/246/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261009 |
| v0.28.0 | cpu | 8/270/4367/539/0 | 4/183/3421/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261009 |
| v0.28.0 | rocm | 26/390/4721/708/0 | 4/183/2848/482/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261009 |
| v0.27.1 | gpu | 8/284/4488/627/0 | 4/181/3421/478/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261009 |
| v0.27.1 | cpu | 8/273/4380/539/0 | 4/184/3425/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261009 |
| v0.27.1 | rocm | 26/391/4745/717/0 | 4/184/2852/492/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261009 |
| v0.27.0 | gpu | 8/284/4488/627/0 | 4/181/3421/478/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261009 |
| v0.27.0 | cpu | 8/273/4380/539/0 | 4/184/3425/438/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261009 |
| v0.27.0 | rocm | 26/391/4745/717/0 | 4/184/2852/492/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261009 |
| v0.26.0 | gpu | 10/291/4512/630/0 | 4/177/3419/479/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261009 |
| v0.26.0 | cpu | 10/280/4423/547/0 | 4/180/3425/439/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261009 |
| v0.26.0 | rocm | 26/388/4745/717/0 | 4/181/2852/492/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261009 |
| v0.25.1 | gpu | 13/366/5119/721/0 | 4/178/3428/479/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261009 |
| v0.25.1 | cpu | 13/355/5034/638/0 | 4/181/3434/439/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261009 |
| v0.25.1 | rocm | 26/399/4822/721/0 | 4/192/2864/492/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261009 |
| v0.25.0 | gpu | 14/367/5120/721/0 | 5/179/3429/479/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261009 |
| v0.25.0 | cpu | 14/356/5035/638/0 | 5/182/3435/439/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261009 |
| v0.25.0 | rocm | 27/400/4823/721/0 | 5/193/2865/492/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261009 |
| v0.24.0 | gpu | 14/382/5187/733/0 | 5/194/3432/479/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261009 |
| v0.24.0 | cpu | 14/369/5062/660/0 | 5/194/3438/439/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261009 |
| v0.24.0 | rocm | 27/409/4856/730/0 | 5/202/2868/493/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261009 |

<!-- scan-summary:end -->
