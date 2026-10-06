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

_Last scanned: 2026-10-06T07:24:18Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/186/4061/342/0 | 5/172/4032/268/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261006 |
| nightly | cpu | 5/232/4252/417/0 | 5/231/4252/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261006 |
| nightly | rocm | 24/357/4633/604/0 | 5/232/3669/453/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261006 |
| v0.31.0 | gpu | 5/186/4061/342/0 | 5/172/4032/268/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261006 |
| v0.31.0 | cpu | 5/233/4252/417/0 | 5/232/4252/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261006 |
| v0.31.0 | rocm | 24/357/4641/604/0 | 5/232/3669/453/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261006 |
| v0.30.0 | gpu | 5/189/4138/343/0 | 5/172/4037/267/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261006 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261006 |
| v0.30.0 | rocm | 24/357/4687/605/0 | 5/232/3674/454/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261006 |
| v0.29.0 | gpu | 6/196/4272/344/0 | 6/179/4054/268/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261006 |
| v0.29.0 | cpu | 7/244/4362/434/0 | 6/239/4269/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261006 |
| v0.29.0 | rocm | 25/364/4740/606/0 | 6/239/3691/455/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261006 |
| v0.28.0 | gpu | 6/203/4454/351/0 | 6/179/4051/268/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261006 |
| v0.28.0 | cpu | 7/244/4416/440/0 | 6/239/4267/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261006 |
| v0.28.0 | rocm | 25/364/4766/609/0 | 6/239/3689/455/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261006 |
| v0.27.1 | gpu | 7/258/4532/528/0 | 6/237/4262/451/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261006 |
| v0.27.1 | cpu | 7/247/4429/440/0 | 6/240/4271/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261006 |
| v0.27.1 | rocm | 25/365/4790/618/0 | 6/240/3693/465/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261006 |
| v0.27.0 | gpu | 7/258/4532/528/0 | 6/237/4262/451/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261006 |
| v0.27.0 | cpu | 7/247/4429/440/0 | 6/240/4271/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261006 |
| v0.27.0 | rocm | 25/365/4790/618/0 | 6/240/3693/465/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261006 |
| v0.26.0 | gpu | 9/265/4556/531/0 | 6/233/4260/452/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261006 |
| v0.26.0 | cpu | 9/254/4472/448/0 | 6/236/4271/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261006 |
| v0.26.0 | rocm | 25/362/4790/618/0 | 6/237/3693/465/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261006 |
| v0.25.1 | gpu | 12/340/5163/622/0 | 6/234/4269/452/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261006 |
| v0.25.1 | cpu | 12/329/5083/539/0 | 6/237/4280/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261006 |
| v0.25.1 | rocm | 25/373/4867/622/0 | 6/248/3705/465/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261006 |
| v0.25.0 | gpu | 13/341/5164/622/0 | 7/235/4270/452/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261006 |
| v0.25.0 | cpu | 13/330/5084/539/0 | 7/238/4281/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261006 |
| v0.25.0 | rocm | 26/374/4868/622/0 | 7/249/3706/465/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261006 |
| v0.24.0 | gpu | 13/356/5231/634/0 | 7/250/4273/452/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261006 |
| v0.24.0 | cpu | 13/343/5111/561/0 | 7/250/4284/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261006 |
| v0.24.0 | rocm | 26/383/4901/631/0 | 7/258/3709/466/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261006 |

<!-- scan-summary:end -->
