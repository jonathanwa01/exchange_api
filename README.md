# exchange_api

A Python project that fetches currency exchange rates from a public API, stores them in a Parquet file, and visualizes them with interactive plots. The application automatically fetches daily updates to keep your data current.

## Features

- **Exchange Rate Fetching**: Retrieves historical and real-time currency exchange rates from a public API
- **Data Storage**: Saves exchange rates in efficient Parquet format
- **Daily Updates**: Automatically fetches and updates exchange data on a daily schedule
- **Interactive Visualization**: Creates interactive plots using Plotly to visualize exchange rate trends
- **Multi-Currency Support**: Track exchange rates for multiple target currencies

## Installation

### Prerequisites

- Python 3.13 or higher
- [UV](https://docs.astral.sh/uv/) package manager

### Installing UV

If you don't have UV installed yet, install it with:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For other installation methods, see the [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/).


### Setup with UV

1. Clone the repository:
```sh
git clone <repository-url>
cd exchange_api
```

2. Install dependencies using UV:
```sh
uv sync
```

This will create a virtual environment and install all required dependencies from `pyproject.toml`.

## Usage

### Initial Data Fetch and Visualization

To fetch historical exchange data and display a visualization:

```sh
uv run src/main.py
```

### Daily Updates

To run the application with automatic daily updates:

```sh
uv run src/daily_fetch.py
```

This will perform an initial data fetch and then continuously check for updates every 24 hours.

## Project Structure

- `src/main.py` - Main entry point with visualization
- `src/daily_fetch.py` - Background daily fetch script
- `src/modules/reader.py` - API client for fetching exchange rates
- `src/modules/visualizer.py` - Plotly visualization utilities
- `data/` - Output directory for Parquet files

## Dependencies

Key dependencies include:
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations
- `requests` - HTTP client for API calls
- `pyarrow` - Parquet file support
- `tqdm` - Progress bars

See `pyproject.toml` for the complete list of dependencies.