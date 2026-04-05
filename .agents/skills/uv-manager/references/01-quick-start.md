# Quick Start

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Create a New Project

```bash
uv init my-project
cd my-project

# Add dependencies
uv add requests fastapi

# Run a script
uv run python main.py

# Install Python (if needed)
uv python install 3.12

# Build and publish
uv build
uv publish
```

## Common Workflows

### New Project
```bash
uv init my-project
cd my-project
uv add requests fastapi
uv run python main.py
```

### Add Dev Dependencies
```bash
uv add --dev pytest pytest-cov
uv add --group lint ruff
uv sync --dev
uv run pytest
```

### Multi-Platform Package
```bash
uv init my-lib --lib
cd my-lib
uv add pydantic "numpy>=1.26"
uv lock
uv build
uv publish
```

### Workspace Project
```bash
uv init workspace-root
cd workspace-root
uv init packages/lib-a
uv init packages/lib-b
uv add lib-a  # Auto-adds to workspace
uv add --with lib-b lib-c
```

### Script with Dependencies
```bash
# Create script.py with PEP 723 metadata
uv run script.py
```

### Global Tool Installation
```bash
uv tool install black
uv tool install ruff
black myproject/
ruff check myproject/
```

### Legacy pip Migration
```bash
# Convert requirements.txt
uv pip compile requirements.in -o requirements.txt

# Install from requirements.txt
uv pip sync requirements.txt

# Or migrate to project
uv init
uv add -r requirements.txt
```
