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

_Last scanned: 2026-10-17T05:51:51Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 0/96/3213/308/0 | 0/82/3184/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261017 |
| nightly | cpu | 3/222/3247/615/0 | 3/221/3247/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261017 |
| nightly | rocm | 25/429/4385/874/0 | 3/222/2592/651/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261017 |
| v0.31.0 | gpu | 5/168/4129/386/0 | 0/82/3184/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261017 |
| v0.31.0 | cpu | 3/223/3267/615/0 | 3/222/3247/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261017 |
| v0.31.0 | rocm | 25/429/4395/874/0 | 3/222/2592/651/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261017 |
| v0.30.0 | gpu | 5/206/4369/421/0 | 0/82/3189/233/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261017 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261017 |
| v0.30.0 | rocm | 25/429/4441/875/0 | 3/222/2597/652/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261017 |
| v0.29.0 | gpu | 6/213/4503/422/0 | 1/89/3206/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261017 |
| v0.29.0 | cpu | 8/316/4162/704/0 | 4/229/3255/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261017 |
| v0.29.0 | rocm | 26/436/4494/876/0 | 4/229/2614/653/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261017 |
| v0.28.0 | gpu | 6/220/4686/429/0 | 1/89/3204/234/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261017 |
| v0.28.0 | cpu | 8/316/4217/710/0 | 4/229/3254/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261017 |
| v0.28.0 | rocm | 26/436/4521/879/0 | 4/229/2613/653/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261017 |
| v0.27.1 | gpu | 8/330/4342/798/0 | 4/227/3258/649/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261017 |
| v0.27.1 | cpu | 8/319/4230/710/0 | 4/230/3258/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261017 |
| v0.27.1 | rocm | 26/437/4545/888/0 | 4/230/2617/663/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261017 |
| v0.27.0 | gpu | 8/330/4342/798/0 | 4/227/3258/649/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261017 |
| v0.27.0 | cpu | 8/319/4230/710/0 | 4/230/3258/609/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261017 |
| v0.27.0 | rocm | 26/437/4545/888/0 | 4/230/2617/663/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261017 |
| v0.26.0 | gpu | 10/337/4366/801/0 | 4/223/3256/650/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261017 |
| v0.26.0 | cpu | 10/326/4273/718/0 | 4/226/3258/610/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261017 |
| v0.26.0 | rocm | 26/434/4545/888/0 | 4/227/2617/663/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261017 |
| v0.25.1 | gpu | 13/412/4973/892/0 | 4/224/3265/650/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261017 |
| v0.25.1 | cpu | 13/401/4884/809/0 | 4/227/3267/610/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261017 |
| v0.25.1 | rocm | 26/445/4622/892/0 | 4/238/2629/663/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261017 |
| v0.25.0 | gpu | 14/413/4974/892/0 | 5/225/3266/650/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261017 |
| v0.25.0 | cpu | 14/402/4885/809/0 | 5/228/3268/610/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261017 |
| v0.25.0 | rocm | 27/446/4623/892/0 | 5/239/2630/663/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261017 |
| v0.24.0 | gpu | 14/428/5041/904/0 | 5/240/3269/650/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261017 |
| v0.24.0 | cpu | 14/415/4912/831/0 | 5/240/3271/610/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261017 |
| v0.24.0 | rocm | 27/455/4656/901/0 | 5/248/2633/664/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261017 |

<!-- scan-summary:end -->
