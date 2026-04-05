# pip Interface

## `uv pip install` - Install packages

```bash
uv pip install requests          # Install package
uv pip install -r requirements.txt  # From file
uv pip install -e ./local-package  # Editable
uv pip install --constraints constraints.txt
uv pip install --overrides overrides.txt
uv pip install --system           # Install to system Python
uv pip install --break-system-packages  # Allow system modification
uv pip install --target /path     # Install to directory
uv pip install --prefix /path     # Install with structure
uv pip install --no-deps          # No dependencies
uv pip install --no-build        # No source builds
uv pip install --only-binary :all:  # Only wheels
uv pip install --python-version 3.11  # For specific version
uv pip install --python-platform linux  # For specific platform
uv pip install --strict           # Validate after install
uv pip install --dry-run          # Don't actually install
```

---

## `uv pip uninstall` - Uninstall packages

```bash
uv pip uninstall requests
uv pip uninstall requests flask
```

---

## `uv pip compile` - Compile requirements

```bash
uv pip compile requirements.in   # To requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip compile requirements.in --format pylock.toml
uv pip compile requirements.in --generate-hashes
uv pip compile requirements.in --universal  # Multi-platform
uv pip compile requirements.in --python-platform linux
uv pip compile requirements.in --no-strip-markers
uv pip compile requirements.in --no-strip-extras
```

---

## `uv pip sync` - Sync requirements

```bash
uv pip sync requirements.txt
uv pip sync requirements.txt --python 3.11
uv pip sync requirements.txt --system
```

---

## `uv pip freeze` - Freeze environment

```bash
uv pip freeze                    # List installed packages
```

---

## `uv pip list` - List packages

```bash
uv pip list                      # Tabular output
uv pip list --format json        # JSON output
```

---

## `uv pip show` - Show package info

```bash
uv pip show requests
```

---

## `uv pip tree` - Show dependency tree

```bash
uv pip tree
uv pip tree --package requests
```

---

## `uv pip check` - Verify environment

```bash
uv pip check                     # Check for conflicts
```

---

## `uv pip download` - Download packages

```bash
uv pip download requests -d ./downloads
```

---

## `uv pip wheel` - Build wheels

```bash
uv pip wheel requests -w ./wheels
```
