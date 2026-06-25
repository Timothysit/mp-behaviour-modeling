# Modelling Behaviour in Matching Pennies

A Quarto website walking through behavioural models fit to matching pennies data.
Notebooks cover synthetic data generation, GLM-HMM, Q-learning, and model comparison.

## Setup (macOS)

### Prerequisites

**[Homebrew](https://brew.sh)** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**[uv](https://docs.astral.sh/uv/)** — Python package manager:
```bash
brew install uv
```

**[Quarto](https://quarto.org)** — notebook rendering:
```bash
brew install --cask quarto
```

### Python environment

Clone the repo and set up the environment:
```bash
git clone <repo-url>
cd mp-behaviour-modeling

uv sync
```

Register the Jupyter kernel so Quarto can find it:
```bash
uv run python -m ipykernel install --user --name mp-behaviour-modeling
```

### Render the site

```bash
quarto render
```

Output is written to `docs/`. To preview with a live server:
```bash
quarto preview
```
