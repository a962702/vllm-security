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

_Last scanned: 2026-10-10T07:02:18Z_ · [Full dashboard](https://a962702.github.io/vllm-security/)

| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |
|---|---|---|---|---|---|
| nightly | gpu | 5/156/4039/322/0 | 5/142/4010/248/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:nightly-20261010 |
| nightly | cpu | 3/184/3392/452/0 | 3/183/3392/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:nightly-20261010 |
| nightly | rocm | 25/391/4579/711/0 | 3/184/2809/488/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:nightly-20261010 |
| v0.31.0 | gpu | 5/156/4048/322/0 | 5/142/4010/248/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.31.0-20261010 |
| v0.31.0 | cpu | 3/185/3400/452/0 | 3/184/3392/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.31.0-20261010 |
| v0.31.0 | rocm | 25/391/4587/711/0 | 3/184/2809/488/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.31.0-20261010 |
| v0.30.0 | gpu | 5/194/4288/357/0 | 5/142/4015/247/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.30.0-20261010 |
| v0.30.0 | cpu | 0/7/7/0/0 | 0/7/7/0/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.30.0-20261010 |
| v0.30.0 | rocm | 25/391/4633/712/0 | 3/184/2814/489/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.30.0-20261010 |
| v0.29.0 | gpu | 6/201/4422/358/0 | 6/149/4032/248/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.29.0-20261010 |
| v0.29.0 | cpu | 8/278/4299/541/0 | 4/191/3404/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.29.0-20261010 |
| v0.29.0 | rocm | 26/398/4686/713/0 | 4/191/2831/490/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.29.0-20261010 |
| v0.28.0 | gpu | 6/208/4604/365/0 | 6/149/4029/248/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.28.0-20261010 |
| v0.28.0 | cpu | 8/278/4353/547/0 | 4/191/3402/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.28.0-20261010 |
| v0.28.0 | rocm | 26/398/4712/716/0 | 4/191/2829/490/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.28.0-20261010 |
| v0.27.1 | gpu | 8/292/4474/635/0 | 4/189/3402/486/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.1-20261010 |
| v0.27.1 | cpu | 8/281/4366/547/0 | 4/192/3406/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.1-20261010 |
| v0.27.1 | rocm | 26/399/4736/725/0 | 4/192/2833/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.1-20261010 |
| v0.27.0 | gpu | 8/292/4474/635/0 | 4/189/3402/486/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.27.0-20261010 |
| v0.27.0 | cpu | 8/281/4366/547/0 | 4/192/3406/446/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.27.0-20261010 |
| v0.27.0 | rocm | 26/399/4736/725/0 | 4/192/2833/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.27.0-20261010 |
| v0.26.0 | gpu | 10/299/4498/638/0 | 4/185/3400/487/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.26.0-20261010 |
| v0.26.0 | cpu | 10/288/4409/555/0 | 4/188/3406/447/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.26.0-20261010 |
| v0.26.0 | rocm | 26/396/4736/725/0 | 4/189/2833/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.26.0-20261010 |
| v0.25.1 | gpu | 13/374/5105/729/0 | 4/186/3409/487/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.1-20261010 |
| v0.25.1 | cpu | 13/363/5020/646/0 | 4/189/3415/447/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.1-20261010 |
| v0.25.1 | rocm | 26/407/4813/729/0 | 4/200/2845/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.1-20261010 |
| v0.25.0 | gpu | 14/375/5106/729/0 | 5/187/3410/487/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.25.0-20261010 |
| v0.25.0 | cpu | 14/364/5021/646/0 | 5/190/3416/447/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.25.0-20261010 |
| v0.25.0 | rocm | 27/408/4814/729/0 | 5/201/2846/500/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.25.0-20261010 |
| v0.24.0 | gpu | 14/390/5173/741/0 | 5/202/3413/487/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai:v0.24.0-20261010 |
| v0.24.0 | cpu | 14/377/5048/668/0 | 5/202/3419/447/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-cpu:v0.24.0-20261010 |
| v0.24.0 | rocm | 27/417/4847/738/0 | 5/210/2849/501/0 | ok | ghcr.io/a962702/vllm-security/vllm-openai-rocm:v0.24.0-20261010 |

<!-- scan-summary:end -->
