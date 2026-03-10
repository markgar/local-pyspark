# fab CLI Reference

Microsoft Fabric CLI (`fab`) — manage Fabric workspaces, items, and files from the command line.

**Important:** Always use `-f` (force) on commands that support it to skip confirmation prompts. The CLI runs non-interactively — there is no way to send keystrokes to respond to prompts.

## Path Format

Paths use dot-notation: `<workspace>.Workspace/<item>.<Type>`. Lakehouse sub-paths extend further: `<lh>.Lakehouse/Files/<path>` or `Tables/<table>`.

Use `-f` on most commands to skip confirmation prompts.

## Authentication

```bash
fab auth login          # Log in (interactive browser flow)
fab auth status         # Show current auth state
fab auth logout         # Log out
```

## Navigation

```bash
fab cd <path>           # Change working directory
fab pwd                 # Print working directory
```

## Listing & Querying

```bash
fab ls                          # List all workspaces
fab ls <ws>.Workspace           # List items in a workspace
fab ls <ws>.Workspace/<lh>.Lakehouse/Tables   # List tables
fab ls -l                       # Long/detailed listing
fab ls -q "[?contains(name, 'Report')]"       # Filter with JMESPath

fab get <path>                  # Get item properties (JSON)
fab get <path> -q id            # Query a specific property
fab get <path> -q .             # Get all properties

fab exists <path>               # Check if workspace/item exists
fab desc <path>                 # Show supported commands for a path/type
```

## Create

```bash
fab mkdir <ws>.Workspace                          # Create workspace
fab mkdir <ws>.Workspace/<nb>.Notebook             # Create empty notebook
fab mkdir <ws>.Workspace/<lh>.Lakehouse/Files/dir  # Create directory in lakehouse
```

## Import & Export

```bash
fab import "<ws>.Workspace/<item>.<Type>" -i <local_path> -f    # Import (create/update)
fab export "<ws>.Workspace/<item>.<Type>" -o <local_dir> -f     # Export to local
fab export "<ws>.Workspace" -o <local_dir> -f                   # Export all items
```

Notebooks support `--format` flag for `.ipynb` or `.py`.

## Copy, Move & Delete

```bash
fab cp <from> <to> -f           # Copy item or file (-r for recursive)
fab mv <from> <to> -f           # Move/rename item or file (-r for recursive)
fab rm <path> -f                # Delete item, file, or table
```

## File Operations (Lakehouse)

```bash
fab cp local.csv "<ws>.Workspace/<lh>.Lakehouse/Files/data/local.csv" -f   # Upload file
fab cp "<ws>.Workspace/<lh>.Lakehouse/Files/data/file.csv" ./file.csv -f   # Download file
fab mkdir "<ws>.Workspace/<lh>.Lakehouse/Files/newdir"                      # Create directory
```

## Shortcuts

```bash
fab ln <target_path> <shortcut_path>    # Create a shortcut
```

## Item Properties

```bash
fab set <path> -q displayName -i "new_name"     # Rename item/workspace
fab set <path> -q <json_path> -i <value> -f     # Set a property
```

## Jobs

```bash
fab job start <item_path>                        # Run async
fab job run <item_path>                          # Run sync (blocks until done)
fab job run <item_path> --timeout 60             # Sync with timeout (seconds)
fab job run-cancel <item_path> --id <job_id>     # Cancel a running job
```

Jobs support `-P` for parameters and `-C`/`-i` for JSON config/input payloads.

## Delta Tables

```bash
fab table load <lh>.Lakehouse/Tables/<tbl> -i <file>   # Load data into table
fab table schema <lh>.Lakehouse/Tables/<tbl>            # Show table schema
fab table optimize <lh>.Lakehouse/Tables/<tbl>          # Optimize table
fab table vacuum <lh>.Lakehouse/Tables/<tbl>            # Vacuum old files
```

## Access Control (Admin)

```bash
fab acl ls <path>               # List ACLs
fab acl get <path>              # Get ACL details
fab acl set <path>              # Set ACLs
fab acl rm <path>               # Remove ACL
```

## Capacity & Resources

```bash
fab assign <path>               # Assign capacity/resource to workspace
fab unassign <path>             # Unassign resource
fab start <path>                # Start a resource
fab stop <path>                 # Stop a resource
```

## Raw API

```bash
fab api workspaces                                      # GET workspaces
fab api -X post <endpoint> -i '{"key":"value"}'         # POST with body
fab api <endpoint> -A storage                           # Use storage audience token
fab api <endpoint> -q <jmespath>                        # Filter response
```

## Configuration

```bash
fab config ls                                   # List all config
fab config get <key>                            # Get config value
fab config set <key> <value>                    # Set config value
fab config set mode interactive                 # Enable interactive mode
fab config clear-cache                          # Clear CLI cache
```
