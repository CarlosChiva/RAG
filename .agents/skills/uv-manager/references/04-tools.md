# Tools (Global Commands)

## `uv tool run` / `uvx` - Run tools

```bash
uv tool run black -- version     # Run black
uvx black -- version             # Shorter alias
uv tool run --with requests httpx  # With temporary dependency
uvx --from requests httpx        # Alias syntax
```

---

## `uv tool install` - Install global tools

```bash
uv tool install black            # Install to ~/.local/bin
uv tool install black==23.1.0    # Specific version
uv tool install --python 3.11 black  # Use specific Python
uv tool install --upgrade black  # Upgrade
uv tool install --force black    # Reinstall
```

---

## `uv tool upgrade` - Upgrade tools

```bash
uv tool upgrade                  # Upgrade all tools
uv tool upgrade black            # Upgrade specific tool
```

---

## `uv tool list` - List installed tools

```bash
uv tool list
```
