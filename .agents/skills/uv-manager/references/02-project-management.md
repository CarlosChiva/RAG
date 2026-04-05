# Project Management Commands

## `uv init` - Create a new project

```bash
uv init                          # Initialize in current directory
uv init my-project               # Initialize in new directory
uv init --lib                    # Create a library (src layout)
uv init --template <url>         # Use a template repository
uv init --no-readme              # Don't create README.md
uv init --no-git                 # Don't initialize git repository
```

**Creates:** `pyproject.toml`, `.python-version`, `.venv`, `uv.lock`, and `src/` or project files

---

## `uv add` - Add dependencies

```bash
uv add requests                  # Add to project dependencies
uv add requests>=2.28            # With version constraint
uv add --dev pytest              # Add to dev dependencies
uv add --group test pytest       # Add to custom dependency group
uv add --optional docs sphinx    # Add to optional dependency (extra)
uv add git+https://github.com/org/repo.git  # From Git
uv add ./local-package           # From local path
uv add --editable ./local-package # Editable install
uv add --with black mypackage    # Add package with temporary dependency
uv add --python 3.11 requests    # Specify Python version
```

**Dependency sources:**
- PyPI: `requests>=2.28,<3.0`
- Git: `git+https://github.com/org/repo.git@branch#subdirectory=src`
- URL: `https://example.com/package-1.0.tar.gz`
- Path: `./local-package` or `file://./local-package`
- Workspace: `{ workspace = true }` in `tool.uv.sources`

---

## `uv remove` - Remove dependencies

```bash
uv remove requests
uv remove --dev pytest
uv remove --group test pytest
```

---

## `uv sync` - Sync environment

```bash
uv sync                          # Sync all dependencies
uv sync --dev                    # Include dev dependencies
uv sync --group test             # Include specific group
uv sync --extra docs             # Include optional dependency
uv sync --all-extras             # Include all extras
uv sync --frozen                 # Don't update lockfile
uv sync --locked                 # Fail if lockfile needs update
uv sync --no-sync                # Skip sync (for use with --with)
uv sync --python 3.11            # Use specific Python version
```

---

## `uv lock` - Update lockfile

```bash
uv lock                          # Resolve and lock dependencies
uv lock --python 3.11            # Lock for specific Python version
uv lock --upgrade                # Allow upgrades
uv lock --upgrade-package requests  # Upgrade specific package
```

---

## `uv export` - Export lockfile

```bash
uv export                        # Export as requirements.txt
uv export --format requirements.txt
uv export --format pylock.toml   # Modern lockfile format
uv export --format cyclonedx1.5  # CycloneDX SBOM format
uv export --dev                  # Include dev dependencies
uv export --group test
uv export --all-extras
uv export --no-dev               # Exclude dev dependencies
uv export --package mypackage    # Export specific workspace package
uv export --prune requests       # Remove package from output
uv export --no-annotate          # No source annotations
uv export --no-header            # No comment header
uv export --no-editable          # Export editables as paths
uv export --no-hashes            # Omit hashes
uv export -o requirements.txt    # Output to file
```

---

## `uv tree` - Show dependency tree

```bash
uv tree                          # Show all dependencies
uv tree --dev                    # Include dev dependencies
uv tree --package requests       # Show specific package tree
```

---

## `uv version` - Bump project version

```bash
uv version                       # Show current version
uv version patch                 # Bump patch (1.0.0 -> 1.0.1)
uv version minor                 # Bump minor (1.0.0 -> 1.1.0)
uv version major                 # Bump major (1.0.0 -> 2.0.0)
uv version 1.2.3                 # Set specific version
```

---

## `uv audit` - Check for vulnerabilities

```bash
uv audit                         # Check current project
uv audit --dev                   # Include dev dependencies
uv audit --format json           # JSON output
```

---

## `uv format` - Format code

```bash
uv format                        # Format project files
uv format --check                # Check without modifying
```
