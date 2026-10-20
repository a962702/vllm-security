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

_Last scanned: 2026-10-20T05:45:30Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 11/316/2513/726/0 | 11/302/2484/652/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261020 |
| nightly | cpu | 16/466/2369/1102/0 | 16/466/2369/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261020 |
| nightly | rocm | 17/467/1713/1146/0 | 17/467/1713/1146/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261020 |
| v0.32.0 | gpu | 11/316/2513/726/0 | 11/302/2484/652/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.32.0-20261020 |
| v0.32.0 | cpu | 16/466/2369/1102/0 | 16/466/2369/1101/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.32.0-20261020 |
| v0.32.0 | rocm | 39/675/3508/1367/0 | 17/467/1714/1143/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.32.0-20261020 |
| v0.31.0 | gpu | 19/424/3357/841/0 | 12/304/2484/653/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261020 |
| v0.31.0 | cpu | 16/470/2389/1108/0 | 16/469/2369/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261020 |
| v0.31.0 | rocm | 39/677/3516/1368/0 | 17/469/1714/1144/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261020 |
| v0.30.0 | gpu | 19/464/3591/880/0 | 12/304/2489/652/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261020 |
| v0.30.0 | cpu | 0/9/7/1/0 | 0/9/7/1/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261020 |
| v0.30.0 | rocm | 39/677/3562/1369/0 | 17/469/1719/1145/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261020 |
| v0.29.0 | gpu | 20/471/3725/881/0 | 13/311/2506/653/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261020 |
| v0.29.0 | cpu | 21/564/3282/1198/0 | 17/476/2377/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261020 |
| v0.29.0 | rocm | 40/684/3615/1370/0 | 18/476/1736/1146/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261020 |
| v0.28.0 | gpu | 20/482/3899/893/0 | 13/311/2504/653/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261020 |
| v0.28.0 | cpu | 21/564/3337/1204/0 | 17/476/2376/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261020 |
| v0.28.0 | rocm | 39/684/3642/1373/0 | 17/476/1735/1146/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261020 |
| v0.27.1 | gpu | 22/578/3462/1292/0 | 18/474/2380/1142/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261020 |
| v0.27.1 | cpu | 21/567/3350/1204/0 | 17/477/2380/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261020 |
| v0.27.1 | rocm | 39/685/3666/1382/0 | 17/477/1739/1156/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261020 |
| v0.27.0 | gpu | 22/578/3462/1292/0 | 18/474/2380/1142/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261020 |
| v0.27.0 | cpu | 21/567/3350/1204/0 | 17/477/2380/1102/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261020 |
| v0.27.0 | rocm | 39/685/3666/1382/0 | 17/477/1739/1156/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261020 |
| v0.26.0 | gpu | 24/585/3486/1295/0 | 18/470/2378/1143/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261020 |
| v0.26.0 | cpu | 23/574/3393/1212/0 | 17/473/2380/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261020 |
| v0.26.0 | rocm | 39/682/3666/1382/0 | 17/474/1739/1156/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261020 |
| v0.25.1 | gpu | 27/660/4094/1386/0 | 18/471/2387/1143/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261020 |
| v0.25.1 | cpu | 26/649/4005/1303/0 | 17/474/2389/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261020 |
| v0.25.1 | rocm | 39/693/3743/1386/0 | 17/485/1751/1156/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261020 |
| v0.25.0 | gpu | 28/661/4095/1386/0 | 19/472/2388/1143/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261020 |
| v0.25.0 | cpu | 27/650/4006/1303/0 | 18/475/2390/1103/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261020 |
| v0.25.0 | rocm | 40/694/3744/1386/0 | 18/486/1752/1156/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261020 |

<!-- scan-summary:end -->
