# Key Concepts

**Lockfile (`uv.lock`):** Contains resolved dependency graph with exact versions, hashes, and platform-specific resolutions. Managed by uv, not edited manually.

**Dependency Groups (PEP 735):** Replaces `dev-dependencies`. Use `[dependency-groups]` in pyproject.toml for named groups like `test`, `lint`, `docs`.

**Extras (Optional Dependencies):** Defined in `project.optional-dependencies`. Installed with `--extra` or `--all-extras`.

**Sources (`tool.uv.sources`):** Override where packages come from. Supports path, git, url, workspace, and registry sources.

**Editable Installs:** Default for workspace members and path sources. Use `--editable` flag or `editable = true` in sources.

**Markers:** Platform/Python version conditions like `python_version >= "3.11"` or `sys_platform == "win32"`.

**Seed Packages:** `pip`, `setuptools`, and `wheel` can be pre-installed in venvs with `--seed`.

**Universal Lockfiles:** Single lockfile supporting multiple platforms/Python versions. Use `--universal` in pip compile.
