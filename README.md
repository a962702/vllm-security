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

_Last scanned: 2026-10-13T07:43:25Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/161/4002/350/0 | 5/147/3973/276/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261013 |
| nightly | cpu | 3/206/3268/506/0 | 3/205/3268/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261013 |
| nightly | rocm | 25/413/4471/765/0 | 3/206/2685/542/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261013 |
| v0.31.0 | gpu | 5/161/4023/350/0 | 5/147/3973/276/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261013 |
| v0.31.0 | cpu | 3/207/3288/506/0 | 3/206/3268/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261013 |
| v0.31.0 | rocm | 25/413/4479/765/0 | 3/206/2685/542/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261013 |
| v0.30.0 | gpu | 5/199/4263/385/0 | 5/147/3978/275/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261013 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261013 |
| v0.30.0 | rocm | 25/413/4525/766/0 | 3/206/2690/543/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261013 |
| v0.29.0 | gpu | 6/206/4397/386/0 | 6/154/3995/276/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261013 |
| v0.29.0 | cpu | 8/300/4187/595/0 | 4/213/3280/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261013 |
| v0.29.0 | rocm | 26/420/4578/767/0 | 4/213/2707/544/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261013 |
| v0.28.0 | gpu | 6/213/4579/393/0 | 6/154/3992/276/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261013 |
| v0.28.0 | cpu | 8/300/4241/601/0 | 4/213/3278/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261013 |
| v0.28.0 | rocm | 26/420/4604/770/0 | 4/213/2705/544/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261013 |
| v0.27.1 | gpu | 8/314/4362/689/0 | 4/211/3278/540/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261013 |
| v0.27.1 | cpu | 8/303/4254/601/0 | 4/214/3282/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261013 |
| v0.27.1 | rocm | 26/421/4628/779/0 | 4/214/2709/554/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261013 |
| v0.27.0 | gpu | 8/314/4362/689/0 | 4/211/3278/540/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261013 |
| v0.27.0 | cpu | 8/303/4254/601/0 | 4/214/3282/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261013 |
| v0.27.0 | rocm | 26/421/4628/779/0 | 4/214/2709/554/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261013 |
| v0.26.0 | gpu | 10/321/4386/692/0 | 4/207/3276/541/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261013 |
| v0.26.0 | cpu | 10/310/4297/609/0 | 4/210/3282/501/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261013 |
| v0.26.0 | rocm | 26/418/4628/779/0 | 4/211/2709/554/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261013 |
| v0.25.1 | gpu | 13/396/4993/783/0 | 4/208/3285/541/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261013 |
| v0.25.1 | cpu | 13/385/4908/700/0 | 4/211/3291/501/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261013 |
| v0.25.1 | rocm | 26/429/4705/783/0 | 4/222/2721/554/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261013 |
| v0.25.0 | gpu | 14/397/4994/783/0 | 5/209/3286/541/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261013 |
| v0.25.0 | cpu | 14/386/4909/700/0 | 5/212/3292/501/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261013 |
| v0.25.0 | rocm | 27/430/4706/783/0 | 5/223/2722/554/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261013 |
| v0.24.0 | gpu | 14/412/5061/795/0 | 5/224/3289/541/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261013 |
| v0.24.0 | cpu | 14/399/4936/722/0 | 5/224/3295/501/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261013 |
| v0.24.0 | rocm | 27/439/4739/792/0 | 5/232/2725/555/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261013 |

<!-- scan-summary:end -->
