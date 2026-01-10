# Installation Guide

There are several ways to install and use `vdoc` depending on your needs.

## Option 1: Install via pipx (Recommended)
If you want to use `vdoc` as a command-line tool across multiple projects without polluting your global Python environment, use `pipx`.

```bash
# Install from the local folder (if you are developing it)
pipx install /path/to/vdoc

# Or install from git (if hosted)
pipx install git+https://github.com/yourusername/vdoc.git
```

Now you can run `vdoc init` in any directory.

## Option 2: Install as a Dev Dependency
If you want to enforce a specific version of `vdoc` for a team project, add it to your project's dependencies.

### Using pip
```bash
pip install git+https://github.com/yourusername/vdoc.git
```

### Using uv
```bash
uv add --dev git+https://github.com/yourusername/vdoc.git
```

## Option 3: Local "Editable" Install
If you are modifying `vdoc` and want to test changes immediately in another repo:

1. Navigate to the `vdoc` directory.
2. Install it in editable mode:
   ```bash
   pip install -e .
   ```
   *Note: This makes it available in the current python environment.*
