# Virtual Environments

## `uv venv` - Create virtual environment

```bash
uv venv                          # Create .venv in current dir
uv venv my-venv                  # Create at path
uv venv --python 3.11            # Use specific Python
uv venv --python python3.11      # Use system Python
uv venv --seed                   # Install pip, setuptools, wheel
uv venv --system-site-packages   # Access system site-packages
uv venv --relocatable            # Make relocatable
uv venv --prompt myproject       # Custom prompt prefix
uv venv --clear                  # Remove existing path first
uv venv --allow-existing         # Preserve existing files
```
