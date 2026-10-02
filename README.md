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

_Last scanned: 2026-10-02T06:48:55Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/181/4076/335/0 | 5/167/4047/261/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261002 |
| nightly | cpu | 5/212/4413/337/0 | 5/211/4413/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261002 |
| nightly | rocm | 24/337/4794/524/0 | 5/212/3830/373/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261002 |
| v0.30.0 | gpu | 5/184/4149/336/0 | 5/167/4048/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261002 |
| v0.30.0 | cpu | 0/7/4/0/0 | 0/7/4/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261002 |
| v0.30.0 | rocm | 24/337/4844/525/0 | 5/212/3831/374/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261002 |
| v0.29.0 | gpu | 6/191/4274/336/0 | 6/174/4056/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261002 |
| v0.29.0 | cpu | 7/224/4511/353/0 | 6/219/4418/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261002 |
| v0.29.0 | rocm | 25/344/4888/525/0 | 6/219/3839/374/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261002 |
| v0.28.0 | gpu | 6/198/4459/343/0 | 6/174/4056/260/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261002 |
| v0.28.0 | cpu | 7/224/4567/359/0 | 6/219/4418/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261002 |
| v0.28.0 | rocm | 25/344/4916/528/0 | 6/219/3839/374/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261002 |
| v0.27.1 | gpu | 7/238/4682/447/0 | 6/217/4412/370/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261002 |
| v0.27.1 | cpu | 7/227/4579/359/0 | 6/220/4421/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261002 |
| v0.27.1 | rocm | 25/345/4939/537/0 | 6/220/3842/384/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261002 |
| v0.27.0 | gpu | 7/238/4682/447/0 | 6/217/4412/370/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261002 |
| v0.27.0 | cpu | 7/227/4579/359/0 | 6/220/4421/330/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261002 |
| v0.27.0 | rocm | 25/345/4939/537/0 | 6/220/3842/384/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261002 |
| v0.26.0 | gpu | 9/245/4706/450/0 | 6/213/4410/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261002 |
| v0.26.0 | cpu | 9/234/4622/367/0 | 6/216/4421/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261002 |
| v0.26.0 | rocm | 25/341/4938/537/0 | 6/216/3841/384/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261002 |
| v0.25.1 | gpu | 12/320/5313/541/0 | 6/214/4419/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261002 |
| v0.25.1 | cpu | 12/309/5233/458/0 | 6/217/4430/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261002 |
| v0.25.1 | rocm | 25/352/5015/541/0 | 6/227/3853/384/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261002 |
| v0.25.0 | gpu | 13/321/5314/541/0 | 7/215/4420/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261002 |
| v0.25.0 | cpu | 13/310/5234/458/0 | 7/218/4431/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261002 |
| v0.25.0 | rocm | 26/353/5016/541/0 | 7/228/3854/384/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261002 |
| v0.24.0 | gpu | 13/336/5381/553/0 | 7/230/4423/371/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261002 |
| v0.24.0 | cpu | 13/323/5261/480/0 | 7/230/4434/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261002 |
| v0.24.0 | rocm | 26/362/5049/550/0 | 7/237/3857/385/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261002 |
| v0.23.0 | gpu | 26/358/5432/561/0 | 7/233/4431/372/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.23.0-20261002 |
| v0.23.0 | cpu | 26/345/5312/487/0 | 7/233/4442/331/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.23.0-20261002 |
| v0.23.0 | rocm | 26/366/5074/560/0 | 7/241/3866/385/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.23.0-20261002 |

<!-- scan-summary:end -->
