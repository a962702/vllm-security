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

_Last scanned: 2026-10-15T05:56:27Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 0/90/3190/302/0 | 0/76/3161/228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261015 |
| nightly | cpu | 3/210/3275/584/0 | 3/209/3275/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261015 |
| nightly | rocm | 25/417/4413/843/0 | 3/210/2620/620/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261015 |
| v0.31.0 | gpu | 5/162/4106/380/0 | 0/76/3161/228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261015 |
| v0.31.0 | cpu | 3/211/3295/584/0 | 3/210/3275/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261015 |
| v0.31.0 | rocm | 25/417/4423/843/0 | 3/210/2620/620/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261015 |
| v0.30.0 | gpu | 5/200/4346/415/0 | 0/76/3166/227/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261015 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261015 |
| v0.30.0 | rocm | 25/417/4469/844/0 | 3/210/2625/621/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261015 |
| v0.29.0 | gpu | 6/207/4480/416/0 | 1/83/3183/228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261015 |
| v0.29.0 | cpu | 8/304/4190/673/0 | 4/217/3283/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261015 |
| v0.29.0 | rocm | 26/424/4522/845/0 | 4/217/2642/622/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261015 |
| v0.28.0 | gpu | 6/214/4662/423/0 | 1/83/3180/228/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261015 |
| v0.28.0 | cpu | 8/304/4244/679/0 | 4/217/3281/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261015 |
| v0.28.0 | rocm | 26/424/4548/848/0 | 4/217/2640/622/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261015 |
| v0.27.1 | gpu | 8/318/4369/767/0 | 4/215/3285/618/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261015 |
| v0.27.1 | cpu | 8/307/4257/679/0 | 4/218/3285/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261015 |
| v0.27.1 | rocm | 26/425/4572/857/0 | 4/218/2644/632/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261015 |
| v0.27.0 | gpu | 8/318/4369/767/0 | 4/215/3285/618/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261015 |
| v0.27.0 | cpu | 8/307/4257/679/0 | 4/218/3285/578/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261015 |
| v0.27.0 | rocm | 26/425/4572/857/0 | 4/218/2644/632/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261015 |
| v0.26.0 | gpu | 10/325/4393/770/0 | 4/211/3283/619/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261015 |
| v0.26.0 | cpu | 10/314/4300/687/0 | 4/214/3285/579/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261015 |
| v0.26.0 | rocm | 26/422/4572/857/0 | 4/215/2644/632/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261015 |
| v0.25.1 | gpu | 13/400/5000/861/0 | 4/212/3292/619/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261015 |
| v0.25.1 | cpu | 13/389/4911/778/0 | 4/215/3294/579/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261015 |
| v0.25.1 | rocm | 26/433/4649/861/0 | 4/226/2656/632/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261015 |
| v0.25.0 | gpu | 14/401/5001/861/0 | 5/213/3293/619/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261015 |
| v0.25.0 | cpu | 14/390/4912/778/0 | 5/216/3295/579/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261015 |
| v0.25.0 | rocm | 27/434/4650/861/0 | 5/227/2657/632/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261015 |
| v0.24.0 | gpu | 14/416/5068/873/0 | 5/228/3296/619/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261015 |
| v0.24.0 | cpu | 14/403/4939/800/0 | 5/228/3298/579/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261015 |
| v0.24.0 | rocm | 27/443/4683/870/0 | 5/236/2660/633/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261015 |

<!-- scan-summary:end -->
