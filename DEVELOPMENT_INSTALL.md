# Development Installation Guide

## Installing Dolphain in Development Mode

To use Dolphain in Jupyter notebooks with your virtual environment, you need to install it in "editable" or "development" mode.

### Quick Setup (Already Done! ✅)

```bash
# 1. Activate your virtual environment
source .venv/bin/activate

# 2. Install in development mode
pip install -e .
```

This creates a link to your source code, so any changes you make to the `dolphain/` package are immediately available without reinstalling.

### Verify Installation

```bash
source .venv/bin/activate
python -c "import dolphain; print('Success!')"
```

### Using in Jupyter Notebooks

Now in any Jupyter notebook running with the `.venv` kernel:

```python
import dolphain

# All functions are available
data = dolphain.read_ears_file('data/file.210')
dolphain.plot_overview(data)

# Batch processing works too
files = dolphain.find_data_files('data', '**/*.210')
processor = dolphain.BatchProcessor()
# ...
```

### Setting Up Jupyter Kernel (If Needed)

If Jupyter doesn't see your `.venv`:

```bash
# Activate venv
source .venv/bin/activate

# Install ipykernel
pip install ipykernel

# Register kernel
python -m ipykernel install --user --name=dolphain --display-name "Python (dolphain)"
```

Then in Jupyter:

1. Open your notebook
2. Click "Kernel" → "Change Kernel"
3. Select "Python (dolphain)"

### What `-e` Does

The `-e` flag installs the package in "editable" mode:

- ✅ Changes to code are immediately available
- ✅ No need to reinstall after editing
- ✅ Perfect for development
- ✅ Acts like an installed package

### Project Structure

```
dolphain/
├── setup.py              # Package configuration (newly created)
├── dolphain/             # Your package source
│   ├── __init__.py
│   ├── io.py
│   ├── signal.py
│   ├── plotting.py
│   └── batch.py
└── .venv/                # Virtual environment
```

When installed with `-e`, Python creates a link from `.venv/lib/python3.x/site-packages/` to your `dolphain/` source directory.

### Testing Your Installation

```python
# In a notebook or Python script
import dolphain

# Check what's available
print(dir(dolphain))

# Verify batch processing
print('BatchProcessor available:', hasattr(dolphain, 'BatchProcessor'))

# Test a function
files = dolphain.find_data_files('data', '**/*.210')
print(f'Found {len(files)} files')
```

### Troubleshooting

#### Issue: `ModuleNotFoundError: No module named 'dolphain'`

**Solution:** Make sure you installed in editable mode:

```bash
source .venv/bin/activate
pip install -e .
```

#### Issue: Changes to code not reflected

**Solution:** Restart the Jupyter kernel:

- In notebook: "Kernel" → "Restart"
- Or re-import: `import importlib; importlib.reload(dolphain)`

#### Issue: Wrong Python environment

**Solution:** Check which Python Jupyter is using:

```python
import sys
print(sys.executable)
# Should show: /Users/mjhaas/code/dolphain/.venv/bin/python
```

### Benefits of Development Mode

1. **Live Updates:** Edit code → It's immediately available
2. **No Reinstall:** No need to `pip install` after every change
3. **Same as Production:** Import works exactly like installed package
4. **Easy Testing:** Test changes instantly in notebooks

### Normal vs Development Mode

**Normal installation:**

```bash
pip install .
# Copies files to site-packages
# Need to reinstall after every change
```

**Development installation:**

```bash
pip install -e .
# Creates link to your source directory
# Changes immediately available
```

### You're All Set! ✅

Your Dolphain package is now installed in development mode. You can:

- ✅ Import dolphain in notebooks
- ✅ Use all 15 functions
- ✅ Run batch experiments
- ✅ Edit code and see changes immediately

**Next:** Open `examples/batch_experiments.ipynb` and run it!

```bash
jupyter notebook examples/batch_experiments.ipynb
```
