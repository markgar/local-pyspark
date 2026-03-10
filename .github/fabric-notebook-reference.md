# Fabric Notebook Reference

Guide for creating, formatting, and importing Microsoft Fabric notebooks with the `fab` CLI, including how to build and deploy Python wheel packages.

## Notebook Folder Structure

A Fabric notebook is a folder named `<name>.Notebook` containing two files:

```
<name>.Notebook/
├── .platform                    # Fabric metadata (display name, type)
└── notebook-content.ipynb       # Jupyter notebook with Fabric-specific metadata
```

## `.platform` File

```json
{
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
    "metadata": {
        "type": "Notebook",
        "displayName": "<notebook_display_name>",
        "description": "<description>"
    },
    "config": {
        "version": "2.0",
        "logicalId": "00000000-0000-0000-0000-000000000000"
    }
}
```

## `notebook-content.ipynb` File

Standard Jupyter ipynb (nbformat 4) with Fabric-specific metadata. Key differences from standard Jupyter:

- Uses `kernel_info` (not `kernelspec`)
- Requires `microsoft`, `nteract`, and `spark_compute` blocks in top-level metadata
- Code cells include `metadata.microsoft` with `language` and `language_group`
- Do NOT include `outputs` or `execution_count` on code cells when importing — empty payloads cause import errors

### Required Top-Level Metadata (with default lakehouse)

```json
{
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "language_info": {
            "name": "python"
        },
        "microsoft": {
            "language": "python",
            "language_group": "synapse_pyspark",
            "ms_spell_check": {
                "ms_spell_check_language": "en"
            }
        },
        "nteract": {
            "version": "nteract-front-end@1.0.0"
        },
        "spark_compute": {
            "compute_id": "/trident/default",
            "session_options": {
                "conf": {
                    "spark.synapse.nbs.session.timeout": "1200000"
                }
            }
        },
        "kernel_info": {
            "name": "synapse_pyspark"
        },
        "dependencies": {
            "lakehouse": {
                "known_lakehouses": [
                    {
                        "id": "<lakehouse_guid>"
                    }
                ],
                "default_lakehouse": "<lakehouse_guid>",
                "default_lakehouse_name": "<lakehouse_name>",
                "default_lakehouse_workspace_id": "<workspace_guid>"
            }
        }
    },
    "cells": []
}
```

### Attaching a Default Lakehouse

The `dependencies.lakehouse` block in the notebook metadata controls which lakehouse is attached. All three fields are required:

| Field | Description |
|---|---|
| `default_lakehouse` | The lakehouse item GUID |
| `default_lakehouse_name` | Display name of the lakehouse |
| `default_lakehouse_workspace_id` | GUID of the workspace containing the lakehouse |

The same GUID must also appear in the `known_lakehouses` array.

To discover the GUIDs, use the `fab` CLI:

```bash
# Get the lakehouse item GUID
fab get "<workspace>.Workspace/<lakehouse>.Lakehouse" -q id

# Get the workspace GUID (either of these work)
fab get "<workspace>.Workspace/<lakehouse>.Lakehouse" -q workspaceId
fab get "<workspace>.Workspace" -q id
```

When a default lakehouse is attached:

- **Spark APIs** (`spark.read`, `notebookutils.fs`, `spark.sql`): Use relative paths like `Files/...` and `Tables/...`
- **Non-Spark APIs** (`%pip install`, pandas, standard Python file I/O): Use the local mount point `/lakehouse/default/Files/...` and `/lakehouse/default/Tables/...`

### Cell Formats

**Markdown cell:**
```json
{
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Title\n",
        "Description text."
    ]
}
```

**Code cell:**
```json
{
    "cell_type": "code",
    "metadata": {
        "microsoft": {
            "language": "python",
            "language_group": "synapse_pyspark"
        }
    },
    "source": [
        "df = spark.sql('SELECT 1')\n",
        "df.show()"
    ]
}
```

Note: Each line in `source` should end with `\n` except the last line.

## fab CLI Commands

### Export a notebook
```bash
fab export "<workspace>.Workspace/<notebook>.Notebook" -o tmp/ -f
```

### Import a notebook
```bash
fab import "<workspace>.Workspace/<notebook>.Notebook" -i tmp/<notebook>.Notebook -f
```

### Delete a notebook
```bash
fab rm "<workspace>.Workspace/<notebook>.Notebook" -f
```

### Upload a file to lakehouse Files
```bash
fab cp <local_file> "<workspace>.Workspace/<lakehouse>.Lakehouse/Files/<path>/<filename>" -f
```

### Create a directory in lakehouse
```bash
fab mkdir "<workspace>.Workspace/<lakehouse>.Lakehouse/Files/<path>"
```

The `-f` flag skips confirmation prompts (required for non-interactive use).

## Staging Notebooks for Import

Use `tmp/nb_import/` in this project to stage notebooks before importing. The `tmp/` directory is gitignored. Write the notebook JSON via Python to avoid VS Code's notebook renderer mangling the `.ipynb` file:

```python
import json, os

nb = { ... }  # notebook dict (see template above)
platform = { ... }  # .platform dict (see template above)

base = "tmp/nb_import/<name>.Notebook"
os.makedirs(base, exist_ok=True)

with open(os.path.join(base, "notebook-content.ipynb"), "w") as f:
    json.dump(nb, f, indent=4)
with open(os.path.join(base, ".platform"), "w") as f:
    json.dump(platform, f, indent=4)
```

## Building and Deploying a Python Wheel to Fabric

End-to-end process for packaging Python code as a `.whl`, uploading it to a lakehouse, and referencing it from a Fabric notebook.

### 1. Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "<package-name>"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.setuptools.packages.find]
include = ["<package_name>*"]
```

### 2. Build the wheel

```bash
pip install build -q
python -m build --wheel
```

This produces a file like `dist/<package_name>-0.1.0-py3-none-any.whl`.

### 3. Upload the wheel to lakehouse Files

```bash
fab mkdir "<workspace>.Workspace/<lakehouse>.Lakehouse/Files/libs"
fab cp dist/<package_name>-0.1.0-py3-none-any.whl \
    "<workspace>.Workspace/<lakehouse>.Lakehouse/Files/libs/<package_name>-0.1.0-py3-none-any.whl" -f
```

### 4. Reference the wheel in a Fabric notebook

Use `%pip install` with the `/lakehouse/default/` path in the first code cell:

```python
%pip install /lakehouse/default/Files/libs/<package_name>-0.1.0-py3-none-any.whl --force-reinstall --no-deps -q
```

Then import and use in subsequent cells:

```python
from <package_name> import <module>
```

The `/lakehouse/default/` prefix resolves to whichever lakehouse is attached as the default. The wheel is stored in the lakehouse Files area, so it's shared across all notebooks that attach the same lakehouse.

### Updating the wheel

When you change the package code, bump the version in `pyproject.toml`, rebuild, and re-upload:

```bash
python -m build --wheel
fab cp dist/<package_name>-<new_version>-py3-none-any.whl \
    "<workspace>.Workspace/<lakehouse>.Lakehouse/Files/libs/<package_name>-<new_version>-py3-none-any.whl" -f
```

Update the `%pip install` cell in the notebook to reference the new version.
