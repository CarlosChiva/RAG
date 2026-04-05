# Configuration

## pyproject.toml

### Project metadata

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My project description"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28,<3.0",
    "httpx[http2]>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black",
]
docs = [
    "mkdocs>=1.4",
]

[dependency-groups]
test = [
    "pytest>=7.0",
    "pytest-cov",
]
lint = [
    "ruff>=0.1.0",
]

[project.scripts]
mycli = "myproject.cli:main"

[build-system]
requires = ["uv_build>=0.11.2,<0.12"]
build-backend = "uv_build"
```

### uv-specific settings

```toml
[tool.uv]
# Dependency sources
dev-dependencies = [
    "pytest>=7.0",
]

# Custom dependency sources
[tool.uv.sources]
my-package = { path = "./local", editable = true }
git-package = { git = "https://github.com/org/repo.git", subdirectory = "pkg" }
url-package = { url = "https://example.com/pkg-1.0.tar.gz" }
workspace-pkg = { workspace = true }

# Workspace configuration
[tool.uv.workspace]
members = ["packages/*"]
exclude = ["packages/legacy"]

# Index configuration
[tool.uv.index]
url = "https://my-index.example.com/simple/"
publish-url = "https://my-index.example.com/publish/"

[tool.uv.index.my-private]
url = "https://private.example.com/simple/"
username = "my-user"
password = "my-password"  # Or use auth token

# Resolver configuration
[tool.uv.resolver]
exclude-newer = "2024-01-01T00:00:00Z"
prerelease = "allow"
```

---

## uv.toml (User Configuration)

```toml
# Global cache directory
cache-dir = "~/.cache/uv"

# Python installation directory
python-install-dir = "~/.local/share/uv/python"

# Managed Python
managed-python = true  # Allow uv to manage Python

# Automatic Python downloads
python-downloads = "auto"  # "auto", "manual", or "never"

# Index configuration
default-index = "https://pypi.org/simple"
index = [
    "https://my-private-index.example.com/simple/",
]

# Authentication
[auth]
pypi.org = { token = "MY_TOKEN" }

# Tool installation directory
tool-dir = "~/.local/bin"

# Environment
[env]
UV_SYSTEM_PYTHON = "true"
UV_PYTHON = "3.11"
```

---

## .python-version

```
# Just version
3.11

# Or full path to Python interpreter
/home/user/.local/share/uv/python/cpython-3.11.4-linux-x86_64-gnu/bin/python3
```
