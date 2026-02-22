# Contributing

## Development Setup

```bash
git clone https://github.com/singer-yang/DeepLens.git
cd DeepLens
pip install -e ".[dev]"
```

## Code Style

Format all code with [Ruff](https://docs.astral.sh/ruff/) before submitting:

```bash
ruff format .
```

## Testing

Run the full test suite:

```bash
pytest test/ -v
```

Run a single test file:

```bash
pytest test/test_geolens.py -v
```

Run with coverage:

```bash
pytest test/ --cov=deeplens --cov-report=term-missing
```

## Pull Request Guidelines

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Run `ruff format .` and `pytest test/ -v` before pushing
4. Open a PR with a clear description of the changes

## Building Documentation

```bash
pip install -r docs/requirements.txt
mkdocs serve  # preview at http://127.0.0.1:8000
```
