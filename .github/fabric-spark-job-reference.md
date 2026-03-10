# Fabric Spark Job Definition Reference

Guide for creating, formatting, and deploying Spark Job Definitions (SJDs) to Microsoft Fabric via the REST API V2 format.

## Folder Structure

When exported via `fab export`, an SJD is a folder named `<name>.SparkJobDefinition`:

```
<name>.SparkJobDefinition/
├── .platform                      # Fabric metadata (same schema as notebooks)
└── SparkJobDefinitionV1.json      # Job config (executable, lakehouse, libs, language)
```

## `SparkJobDefinitionV1.json`

```json
{
    "executableFile": "main.py",
    "defaultLakehouseArtifactId": "<lakehouse_guid>",
    "mainClass": "",
    "additionalLakehouseIds": [],
    "retryPolicy": null,
    "commandLineArguments": "",
    "additionalLibraryUris": ["<package_name>-<version>-py3-none-any.whl"],
    "language": "Python",
    "environmentArtifactId": null
}
```

| Field | Description |
|---|---|
| `executableFile` | Filename of the main `.py` file (just the name, not a path) |
| `defaultLakehouseArtifactId` | GUID of the default lakehouse |
| `additionalLibraryUris` | Array of reference library filenames (`.whl`, `.py`, `.jar`) |
| `language` | `"Python"`, `"Scala"`, `"SparkR"` |
| `commandLineArguments` | Space-separated CLI args passed to the job |
| `additionalLakehouseIds` | Array of additional lakehouse GUIDs |
| `environmentArtifactId` | GUID of a Fabric Environment (optional) |
| `retryPolicy` | Retry config object (optional) |

## Deploying via REST API (V2 Format)

The V2 format inlines all files (main `.py`, `.whl` libraries) as base64 in a single API call. No separate storage upload or storage token needed.

### Payload Structure

```json
{
    "definition": {
        "format": "SparkJobDefinitionV2",
        "parts": [
            {
                "path": "SparkJobDefinitionV1.json",
                "payload": "<base64-encoded config JSON>",
                "payloadType": "InlineBase64"
            },
            {
                "path": "Main/<filename>.py",
                "payload": "<base64-encoded .py file>",
                "payloadType": "InlineBase64"
            },
            {
                "path": "Libs/<filename>.whl",
                "payload": "<base64-encoded .whl file>",
                "payloadType": "InlineBase64"
            }
        ]
    }
}
```

All `payload` values are base64-encoded (use `base64.b64encode()` in Python). This works for both `.py` text files and binary `.whl` files.

### Parts Path Convention

| `path` | Purpose |
|---|---|
| `SparkJobDefinitionV1.json` | Job config (always required) |
| `Main/<filename>` | Main executable file |
| `Libs/<filename>` | Reference libraries (`.whl`, `.py`, `.jar`) |

### API Endpoints

Update an existing SJD:

```bash
fab api -X post \
  "workspaces/<workspace_guid>/items/<sjd_guid>/updateDefinition" \
  -i <payload_file>.json
```

Create a new SJD (add `displayName` and `type` at the top level of the payload):

```bash
fab api -X post "workspaces/<workspace_guid>/items" -i <payload_file>.json
```

HTTP 202 = success. On update, any `Libs/` files not included in the new payload are deleted from the SJD.

## Notes

- The `.platform` file uses the same schema as notebooks with `"type": "SparkJobDefinition"`. See the notebook reference for the full template.
- Build a `.whl` with `pip wheel . -w dist/ --no-deps`. This produces `dist/<package_name>-<version>-py3-none-any.whl` from the project's `pyproject.toml`.
- The Fabric item type for `fab` CLI paths is `SparkJobDefinition` (e.g. `"<workspace>.Workspace/<name>.SparkJobDefinition"`).
