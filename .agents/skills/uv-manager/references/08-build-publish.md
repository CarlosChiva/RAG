# Build & Publish

## `uv build` - Build distributions

```bash
uv build                         # Build sdist and wheel
uv build --sdist                 # Build only source dist
uv build --wheel                 # Build only wheel
uv build --all-packages          # Build all workspace packages
uv build --package mypackage     # Build specific package
uv build -o dist                 # Output directory
uv build --clear                 # Clear output directory first
uv build --no-build-isolation    # Don't isolate build
uv build --python 3.11           # Use specific Python
uv build --config-setting key=value  # Pass to build backend
```

---

## `uv publish` - Upload distributions

```bash
uv publish                       # Upload dist/*
uv publish dist/*.whl            # Upload specific files
uv publish --username user --password pass  # Credentials
uv publish --token TOKEN         # Use token
uv publish --index pypi          # Use configured index
uv publish --trusted-publishing  # Use trusted publishing
uv publish --dry-run             # Don't actually upload
uv publish --no-attestations     # Skip attestations
```

**Environment variables:**
- `UV_PUBLISH_USERNAME`
- `UV_PUBLISH_PASSWORD`
- `UV_PUBLISH_TOKEN`
- `UV_PUBLISH_INDEX`
