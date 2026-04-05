# Environment Variables

## Python

- `UV_PYTHON` - Python interpreter to use
- `UV_MANAGED_PYTHON` - Require uv-managed Python
- `UV_NO_MANAGED_PYTHON` - Disable uv-managed Python
- `UV_PYTHON_DOWNLOADS` - "auto", "manual", or "never"
- `UV_PYTHON_INSTALL_DIR` - Python installation directory
- `UV_SYSTEM_PYTHON` - Use system Python

## Cache

- `UV_CACHE_DIR` - Cache directory path
- `UV_NO_CACHE` - Disable cache

## Resolver

- `UV_INDEX_URL` / `UV_DEFAULT_INDEX` - Default package index
- `UV_INDEX` / `UV_EXTRA_INDEX_URL` - Extra indexes
- `UV_FIND_LINKS` - `--find-links` locations
- `UV_INDEX_STRATEGY` - "first-index", "unsafe-first-match", "unsafe-best-match"
- `UV_RESOLUTION` - "highest", "lowest", "lowest-direct"
- `UV_PRERELEASE` - "disallow", "allow", "if-necessary", "explicit", "if-necessary-or-explicit"
- `UV_EXCLUDE_NEWER` - Limit package upload dates
- `UV_CONSTRAINT` - Constraint files
- `UV_OVERRIDE` - Override files

## Installer

- `UV_LINK_MODE` - "clone", "copy", "hardlink", "symlink"
- `UV_NO_BUILD` - Don't build source distributions
- `UV_NO_BINARY` - Don't install wheels

## Publish

- `UV_PUBLISH_URL` - Upload endpoint URL
- `UV_PUBLISH_USERNAME` - Username for upload
- `UV_PUBLISH_PASSWORD` - Password for upload
- `UV_PUBLISH_TOKEN` - Token for upload
- `UV_PUBLISH_INDEX` - Index name for upload

## General

- `UV_OFFLINE` - Disable network access
- `UV_SYSTEM_CERTS` - Use system certificate store
- `UV_CONFIG_FILE` - Path to uv.toml
- `UV_NO_CONFIG` - Disable config discovery
- `UV_NO_PROGRESS` - Hide progress bars
- `UV_COLOR` - "auto", "always", "never"
