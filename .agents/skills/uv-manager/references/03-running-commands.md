# Running Commands

## `uv run` - Run commands in project environment

```bash
uv run python main.py            # Run script
uv run pytest                    # Run command
uv run -- with-args              # Pass args after --
uv run --with black format .     # Run with temporary dependency
uv run --with black -- with-args # With args
uv run --group test pytest       # Include test dependencies
uv run --extra docs mkdocs serve # Include docs extra
uv run --no-dev                  # Exclude dev dependencies
uv run --frozen                  # Don't update lockfile
uv run --locked                  # Fail if lockfile outdated
uv run --python 3.11 script.py   # Use specific Python
uv run script.py --arg1 --arg2   # Pass args to script
```

### PEP 723 Scripts (inline metadata)

```python
#! python
///
{
  "dependencies": [
    "requests>=2.28"
  ]
}
///
import requests
requests.get("https://api.example.com")
```

```bash
uv run script.py                 # Auto-installs dependencies
```
