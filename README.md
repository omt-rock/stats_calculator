<div align="center">

# 📊 Stats Calculator

**A lightweight, educational CLI tool for descriptive statistics — powered by NumPy.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/numpy-%E2%89%A51.24-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Features](#-features) · [Quick Start](#-quick-start) · [Usage](#-usage) · [Project Structure](#-project-structure) · [Testing](#-testing) · [Contributing](#-contributing)

</div>

---

## ✨ Features

- **Descriptive Statistics** — mean, median, standard deviation (sample & population), percentiles (P25 / P50 / P75), min, and max
- **CSV Ingestion** — reads any CSV with a header row; just point it at a column
- **ASCII Histogram** — instant terminal visualization with configurable bin count
- **Matplotlib Plot** — optional graphical histogram via `--plot` (matplotlib stays an optional dependency)
- **Educational Design** — every statistical function includes a manual implementation cross-checked against NumPy with `assert np.isclose(...)`, so you can read the source and *understand* the math
- **Robust Edge-Case Handling** — empty arrays raise clear errors, single-value sample std returns `NaN` with a warning, missing CSV values are dropped with notice
- **Comprehensive Test Suite** — 14 tests covering correctness, edge cases, and I/O with `pytest`

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**

### Installation

```bash
# Clone the repository
git clone https://github.com/omt-rock/stats_calculator.git
cd stats_calculator

# Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage

### Basic — summary statistics + ASCII histogram

```bash
python stats_calc.py your_data.csv --column score
```

**Output:**

```
Summary for 'score'
----------------------------------------
Count               10
Mean                79.10
Median              80.00
Std dev (sample)    14.28
Std dev (population)13.55
Min                 55.00
25th percentile     71.00
50th percentile     80.00
75th percentile     88.75
Max                 100.00
----------------------------------------

Distribution (10 bins)
----------------------------------------
  55.0-  59.5 | ############################################ (1)
  59.5-  64.0 | ############################################ (1)
  64.0-  68.5 |  (0)
  ...
----------------------------------------
```

### Custom bin count

```bash
python stats_calc.py data.csv --column revenue --bins 20
```

### Graphical histogram (requires matplotlib)

```bash
python stats_calc.py data.csv --column score --plot
```

### CLI Reference

| Argument | Required | Default | Description |
|---|---|---|---|
| `csv_path` | ✅ | — | Path to the CSV file |
| `--column` | ✅ | — | Name of the column to analyze |
| `--bins` | ❌ | `10` | Number of histogram bins |
| `--plot` | ❌ | `false` | Show a matplotlib histogram window |

---

## 🏗 Project Structure

```
stats_calculator/
├── stats_calc.py          # CLI entry point — argument parsing & pretty-printing
├── core/
│   ├── __init__.py
│   ├── loader.py          # CSV → NumPy array (header detection, NaN handling)
│   ├── stats.py           # Statistical functions with manual cross-checks
│   └── histogram.py       # Binning, ASCII rendering, matplotlib rendering
├── tests/
│   ├── __init__.py
│   └── test_stats.py      # 14 pytest tests — correctness & edge cases
├── your_data.csv           # Sample dataset for quick experimentation
└── requirements.txt        # numpy, pytest, matplotlib (optional)
```

### Architecture

```
┌──────────────┐     ┌─────────────┐     ┌───────────────┐
│  stats_calc  │────▶│ core.loader │────▶│   CSV file    │
│   (CLI)      │     └─────────────┘     └───────────────┘
│              │
│              │────▶│ core.stats  │  mean, median, std,
│              │     │             │  percentiles, summarize
│              │     └─────────────┘
│              │
│              │────▶│ core.histogram │  compute, ascii,
│              │     │                │  matplotlib render
└──────────────┘     └────────────────┘
```

The codebase follows a clean **separation of concerns**:

| Module | Responsibility |
|---|---|
| `stats_calc.py` | CLI interface — parsing args, formatting output |
| `core/loader.py` | Data I/O — reading CSVs, handling missing values |
| `core/stats.py` | Pure computation — every function is stateless and testable |
| `core/histogram.py` | Visualization — binning logic separated from rendering |

---

## 🧪 Testing

Run the full test suite:

```bash
pytest tests/ -v
```

**What's covered:**

| Test | What it verifies |
|---|---|
| `test_mean` | Correct arithmetic mean on a hand-computable dataset |
| `test_median_even_length` | Median averages two middle values for even-length arrays |
| `test_median_odd_length` | Median picks exact middle for odd-length arrays |
| `test_std_sample_vs_population` | Sample std > population std, values match hand calculation |
| `test_percentiles` | P25, P50, P75 match linear-interpolation results |
| `test_percentile_25_50_75_ordering` | Percentiles are always in ascending order |
| `test_summarize_returns_all_keys` | `summarize()` returns all 10 expected keys |
| `test_histogram_counts_sum_to_n` | Every value lands in exactly one bin |
| `test_histogram_ascii_renders_without_error` | ASCII renderer produces valid output |
| `test_single_value_array_std_is_zero_population` | Population std of one value = 0 |
| `test_single_value_array_std_is_nan_sample` | Sample std of one value = NaN (undefined) |
| `test_empty_array_raises_valueerror` | Empty input raises `ValueError`, not cryptic crash |
| `test_loader_drops_nan_values` | Missing CSV cells are dropped with correct count |
| `test_loader_missing_column_raises` | Non-existent column name → clear `ValueError` |
| `test_loader_missing_file_raises` | Non-existent file path → `FileNotFoundError` |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch** — `git checkout -b feat/my-feature`
3. **Write tests** for any new functionality
4. **Run the suite** — `pytest tests/ -v` — and make sure everything passes
5. **Submit a Pull Request** with a clear description of your changes

### Ideas for Contributions

- [ ] Add **skewness & kurtosis** calculations
- [ ] Support **JSON** and **Parquet** input formats
- [ ] Add a `--output json` flag for machine-readable results
- [ ] Interactive **TUI mode** with [Rich](https://github.com/Textualize/rich)
- [ ] CI pipeline with GitHub Actions

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ and NumPy**

</div>
