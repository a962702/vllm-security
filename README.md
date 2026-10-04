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

_Last scanned: 2026-10-04T06:51:05Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/181/4075/335/0 | 5/167/4046/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261004 |
| nightly | cpu | 5/218/4369/360/0 | 5/217/4369/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261004 |
| nightly | rocm | 24/343/4750/547/0 | 5/218/3786/396/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261004 |
| v0.30.0 | gpu | 5/184/4148/336/0 | 5/167/4047/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261004 |
| v0.30.0 | cpu | 0/7/4/0/0 | 0/7/4/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261004 |
| v0.30.0 | rocm | 24/343/4800/548/0 | 5/218/3787/397/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261004 |
| v0.29.0 | gpu | 6/191/4273/336/0 | 6/174/4055/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261004 |
| v0.29.0 | cpu | 7/230/4467/376/0 | 6/225/4374/353/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261004 |
| v0.29.0 | rocm | 25/350/4844/548/0 | 6/225/3795/397/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261004 |
| v0.28.0 | gpu | 6/198/4458/343/0 | 6/174/4055/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261004 |
| v0.28.0 | cpu | 7/230/4523/382/0 | 6/225/4374/353/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261004 |
| v0.28.0 | rocm | 25/350/4872/551/0 | 6/225/3795/397/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261004 |
| v0.27.1 | gpu | 7/244/4638/470/0 | 6/223/4368/393/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261004 |
| v0.27.1 | cpu | 7/233/4535/382/0 | 6/226/4377/353/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261004 |
| v0.27.1 | rocm | 25/351/4895/560/0 | 6/226/3798/407/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261004 |
| v0.27.0 | gpu | 7/244/4638/470/0 | 6/223/4368/393/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261004 |
| v0.27.0 | cpu | 7/233/4535/382/0 | 6/226/4377/353/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261004 |
| v0.27.0 | rocm | 25/351/4895/560/0 | 6/226/3798/407/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261004 |
| v0.26.0 | gpu | 9/251/4662/473/0 | 6/219/4366/394/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261004 |
| v0.26.0 | cpu | 9/240/4578/390/0 | 6/222/4377/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261004 |
| v0.26.0 | rocm | 25/347/4895/560/0 | 6/222/3798/407/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261004 |
| v0.25.1 | gpu | 12/326/5269/564/0 | 6/220/4375/394/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261004 |
| v0.25.1 | cpu | 12/315/5189/481/0 | 6/223/4386/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261004 |
| v0.25.1 | rocm | 25/358/4972/564/0 | 6/233/3810/407/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261004 |
| v0.25.0 | gpu | 13/327/5270/564/0 | 7/221/4376/394/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261004 |
| v0.25.0 | cpu | 13/316/5190/481/0 | 7/224/4387/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261004 |
| v0.25.0 | rocm | 26/359/4973/564/0 | 7/234/3811/407/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261004 |
| v0.24.0 | gpu | 13/342/5337/576/0 | 7/236/4379/394/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261004 |
| v0.24.0 | cpu | 13/329/5217/503/0 | 7/236/4390/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261004 |
| v0.24.0 | rocm | 26/368/5006/573/0 | 7/243/3814/408/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261004 |
| v0.23.0 | gpu | 26/364/5388/584/0 | 7/239/4387/395/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20261004 |
| v0.23.0 | cpu | 26/351/5268/510/0 | 7/239/4398/354/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20261004 |
| v0.23.0 | rocm | 26/372/5031/583/0 | 7/247/3823/408/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20261004 |

<!-- scan-summary:end -->
