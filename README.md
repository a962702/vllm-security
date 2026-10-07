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

_Last scanned: 2026-10-07T13:09:08Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/188/4055/346/0 | 5/174/4025/272/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261007 |
| nightly | cpu | 2/156/3404/377/0 | 2/155/3404/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261007 |
| nightly | rocm | 24/363/4579/636/0 | 2/156/2821/413/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261007 |
| v0.31.0 | gpu | 5/188/4056/346/0 | 5/174/4025/272/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261007 |
| v0.31.0 | cpu | 2/157/3405/377/0 | 2/156/3404/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261007 |
| v0.31.0 | rocm | 24/363/4587/636/0 | 2/156/2821/413/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261007 |
| v0.30.0 | gpu | 5/191/4133/347/0 | 5/174/4030/271/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261007 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261007 |
| v0.30.0 | rocm | 24/363/4633/637/0 | 2/156/2826/414/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261007 |
| v0.29.0 | gpu | 6/198/4267/348/0 | 6/181/4047/272/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261007 |
| v0.29.0 | cpu | 7/250/4309/466/0 | 3/163/3421/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261007 |
| v0.29.0 | rocm | 25/370/4686/638/0 | 3/163/2843/415/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261007 |
| v0.28.0 | gpu | 6/205/4449/355/0 | 6/181/4044/272/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261007 |
| v0.28.0 | cpu | 7/250/4363/472/0 | 3/163/3419/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261007 |
| v0.28.0 | rocm | 25/370/4712/641/0 | 3/163/2841/415/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261007 |
| v0.27.1 | gpu | 7/264/4479/560/0 | 3/161/3414/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261007 |
| v0.27.1 | cpu | 7/253/4376/472/0 | 3/164/3423/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261007 |
| v0.27.1 | rocm | 25/371/4736/650/0 | 3/164/2845/425/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261007 |
| v0.27.0 | gpu | 7/264/4479/560/0 | 3/161/3414/411/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261007 |
| v0.27.0 | cpu | 7/253/4376/472/0 | 3/164/3423/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261007 |
| v0.27.0 | rocm | 25/371/4736/650/0 | 3/164/2845/425/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261007 |
| v0.26.0 | gpu | 9/271/4503/563/0 | 3/157/3412/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261007 |
| v0.26.0 | cpu | 9/260/4419/480/0 | 3/160/3423/372/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261007 |
| v0.26.0 | rocm | 25/368/4736/650/0 | 3/161/2845/425/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261007 |
| v0.25.1 | gpu | 12/346/5110/654/0 | 3/158/3421/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261007 |
| v0.25.1 | cpu | 12/335/5030/571/0 | 3/161/3432/372/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261007 |
| v0.25.1 | rocm | 25/379/4813/654/0 | 3/172/2857/425/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261007 |
| v0.25.0 | gpu | 13/347/5111/654/0 | 4/159/3422/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261007 |
| v0.25.0 | cpu | 13/336/5031/571/0 | 4/162/3433/372/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261007 |
| v0.25.0 | rocm | 26/380/4814/654/0 | 4/173/2858/425/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261007 |
| v0.24.0 | gpu | 13/362/5178/666/0 | 4/174/3425/412/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261007 |
| v0.24.0 | cpu | 13/349/5058/593/0 | 4/174/3436/372/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261007 |
| v0.24.0 | rocm | 26/389/4847/663/0 | 4/182/2861/426/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261007 |

<!-- scan-summary:end -->
