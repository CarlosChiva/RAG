# Python Management

## `uv python install` - Install Python

```bash
uv python install 3.11           # Install Python 3.11
uv python install 3.11.4         # Specific patch version
uv python install pypy           # Install PyPy
uv python install pypy3.10       # Specific PyPy version
uv python install --default 3.11 # Set as default
uv python install --upgrade      # Upgrade installed versions
uv python install --reinstall    # Reinstall
uv python install --compile-bytecode  # Compile stdlib
```

---

## `uv python list` - List Python versions

```bash
uv python list                   # Show all installed versions
```

---

## `uv python find` - Find Python

```bash
uv python find                   # Find Python for current project
uv python find 3.11              # Find specific version
```

---

## `uv python pin` - Pin Python version

```bash
uv python pin 3.11               # Pin to 3.11 in .python-version
uv python pin 3.11 --resolved    # Write resolved path
uv python pin --global           # Global pin
uv python pin --rm               # Remove pin
```

---

## `uv python uninstall` - Uninstall Python

```bash
uv python uninstall 3.11
uv python uninstall 3.11.4
```

---

## `uv python dir` - Show Python directory

```bash
uv python dir
```

---

## `uv python update-shell` - Update shell PATH

```bash
uv python update-shell
```
