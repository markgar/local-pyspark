# Local PySpark Dev Container

A local-first development workflow for Microsoft Fabric PySpark projects. Write, test, and debug Spark code on your machine, then deploy the exact same code to Fabric — no notebook conversion, no format translation.

The dev container matches the [Fabric Runtime 1.3](https://learn.microsoft.com/fabric/data-engineering/runtime-1-3) environment (Spark, Python, Java, Delta Lake versions), so code that works locally works in Fabric.

## How It Works

1. **Develop locally** in the dev container — run `python main.py` against a local Spark session
2. **Package your code** as a standard Python wheel (`.whl`)
3. **Deploy to Fabric** as a Spark Job Definition — same `.py` file, same package, no conversion

```
┌─────────────────────────┐         ┌──────────────────────────┐
│  Local (dev container)  │         │  Fabric (Spark Job Def)  │
│                         │         │                          │
│  python main.py         │         │  main.py (uploaded)      │
│  pip install -e .       │   ───►  │  .whl (attached as lib)  │
│  local Spark session    │         │  Fabric Spark cluster    │
└─────────────────────────┘         └──────────────────────────┘
         same code, same package
```

## What's Included

Everything is baked into the Docker image for instant startup:

| Component | Version |
|---|---|
| Apache Spark | 3.5.0 |
| Python | 3.11 |
| Java | 11 (OpenJDK) |
| Delta Lake | 3.2.0 |
| pandas | 2.1.4 |
| NumPy | 1.26.4 |
| PyArrow | 14.0.2 |

### CLIs

- **Azure CLI** (`az`) — Azure resource management
- **Fabric CLI** (`fab`) — Microsoft Fabric workspace management
- **GitHub CLI** (`gh`) — repo and PR management

### Dev Tools

- **Jupyter** — notebook support
- **ruff** — Python linter and formatter
- **pytest** — testing
- **jq** — JSON processing
- **azure-identity** — Azure authentication from Python
- **azure-storage-file-datalake** — OneLake / ADLS Gen2 access from Python

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Build the Image

```bash
docker build -t local-pyspark:latest -f .devcontainer/Dockerfile .devcontainer/
```

### Open in Container

1. Open this repo in VS Code
2. **Cmd/Ctrl+Shift+P** → **Dev Containers: Reopen in Container**

### Run the Example

```bash
python main.py
```

## Project Structure

```
.devcontainer/
  Dockerfile            # Image with Spark, Python, Java, all tools baked in
  devcontainer.json     # VS Code container config (extensions, settings)
local_pyspark/          # Your Python package (becomes the .whl)
  __init__.py
  dataframe.py          # Example module
main.py                 # Entry point — runs locally and in Fabric as-is
pyproject.toml          # Package config for building the .whl
```

## Deploying to Fabric

### Spark Job Definition (recommended)

Your `.py` files run identically in both places. No notebook format, no cell conversion, no `%pip install` hacks.

```bash
# 1. Build the wheel
pip wheel . -w dist/ --no-deps

# 2. Deploy main.py + .whl to a Spark Job Definition (single API call)
fab api -X post "workspaces/<workspace_guid>/items/<sjd_guid>/updateDefinition" \
  -i tmp/sjd_payload.json
```

The `.whl` is attached directly to the Spark Job Definition as a reference library — not stored on a lakehouse. The code and its dependencies travel as a single unit.

See [`.github/fabric-spark-job-reference.md`](.github/fabric-spark-job-reference.md) for the payload format and deployment details.

### Fabric Notebook (alternative)

If you need interactive exploration or cell-by-cell execution, you can deploy as a notebook instead. This requires converting your code into notebook cells and uploading the `.whl` to a lakehouse.

See [`.github/fabric-notebook-reference.md`](.github/fabric-notebook-reference.md) for details.

## Using This as a Template

The `.devcontainer/` folder is self-contained. To use this setup in a new project:

1. **Copy the `.devcontainer/` folder** into your project root:

   ```bash
   cp -r /path/to/local-pyspark/.devcontainer /path/to/your-project/
   ```

2. **Build the image** (one-time, unless you change the Dockerfile):

   ```bash
   cd /path/to/your-project
   docker build -t local-pyspark:latest -f .devcontainer/Dockerfile .devcontainer/
   ```

3. **Open your project in VS Code** → **Dev Containers: Reopen in Container**

That's it. Your project now has local PySpark with all the same tools. The `.devcontainer/` folder is self-contained — no other files from this repo are needed.

If the image is already built on your machine, you can skip step 2. Multiple projects can share the same `local-pyspark:latest` image.
