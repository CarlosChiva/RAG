# Workspaces

## Workspace root pyproject.toml

```toml
[project]
name = "workspace-root"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "package-a",  # Dependency on workspace member
    "requests>=2.28",
]

[tool.uv.sources]
package-a = { workspace = true }
requests = { git = "https://github.com/psf/requests" }  # Shared source

[tool.uv.workspace]
members = ["packages/*"]
exclude = ["packages/legacy"]
```

## Workspace member (packages/package-a/pyproject.toml)

```toml
[project]
name = "package-a"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pydantic>=2.0"]

[build-system]
requires = ["uv_build>=0.11.2,<0.12"]
build-backend = "uv_build"
```

## Workspace commands

```bash
cd workspace-root
uv lock                           # Lock entire workspace
uv sync                           # Sync workspace root
uv run --package package-a python script.py  # Run in member
uv build --all-packages           # Build all members
uv export --package package-a     # Export specific member
```
