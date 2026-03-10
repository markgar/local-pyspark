# Copilot Instructions

## Dev Container Environment

- **OS:** Ubuntu 24.04.3 LTS
- **Python:** 3.11.15
- **Java:** OpenJDK 11.0.30
- **Apache Spark:** 3.5.0 (installed at `/opt/spark`)
- **Git:** 2.52.0
- **GitHub CLI (`gh`):** 2.87.3
- **Microsoft Fabric CLI (`fab`):** 1.4.0
- **pip:** 26.0.1

## Key Python Packages

| Package | Version |
|---|---|
| pyspark | 3.5.0 |
| delta-spark | 3.2.0 |
| pandas | 2.1.4 |
| numpy | 1.26.4 |
| pyarrow | 14.0.2 |
| azure-identity | 1.25.2 |
| azure-storage-blob | 12.28.0 |
| azure-storage-file-datalake | 12.23.0 |
| pytest | 9.0.2 |
| ruff | 0.15.5 |
| jupyterlab | 4.5.5 |
| notebook | 7.5.4 |
| ipykernel | 7.2.0 |
| ms-fabric-cli | 1.4.0 |

## System CLI Tools

curl, wget, gh, git, fab, ssh, scp, rsync, gpg, zip, unzip, tar, gzip, bzip2, xz, find, grep, tree, ps, lsof, netstat, top

## Temporary Files

Use the `tmp/` directory at the workspace root (`/workspaces/local-pyspark/tmp/`) for temporary file import/export prep. This includes staging notebooks, data files, or other artifacts before importing to or after exporting from external services (e.g., Microsoft Fabric). The `tmp/` directory is gitignored and safe for transient content.

## Microsoft Fabric CLI

See [`.github/fab-cli-reference.md`](.github/fab-cli-reference.md) for the `fab` CLI command reference. Covers authentication, workspace/item management, file operations, jobs, and more. The CLI runs non-interactively — always use `-f` to skip prompts.

## Microsoft Fabric Notebooks

See [`.github/fabric-notebook-reference.md`](.github/fabric-notebook-reference.md) for the complete guide on creating, formatting, and importing Fabric notebooks with the `fab` CLI. That document includes the required metadata structure, how to attach a default lakehouse, cell formats, and all relevant `fab` commands.

## Microsoft Fabric Spark Job Definitions

See [`.github/fabric-spark-job-reference.md`](.github/fabric-spark-job-reference.md) for the complete guide on creating, deploying, and running Spark Job Definitions in Fabric. Covers the SJD folder structure, `SparkJobDefinitionV1.json` config format, deploying via the REST API V2 format (inline base64 for `.py` and `.whl` files), and all relevant `fab` CLI commands.
