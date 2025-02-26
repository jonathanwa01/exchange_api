from datetime import datetime
import os
import threading
import time
import pandas as pd
from modules.reader import CurrencyReader
from modules.visualizer import Visualizer

CHECKINTERVALL = 24 * 60 * 60
OUTPUT_FILE = "data/exchange.parquet"
CURRENCIES: list[str] = [
    "Australian Dollar",
    "US Dollar",
    "Israeli Shekel",
    "Cuban Peso",
    "Japanese Yen",
]
START_CURRENCY = "Euro"


def initial_fetch_exchange(r: CurrencyReader) -> None:
    """
    Initially fetches the exchange rate data

    Args:
        r (CurrencyReader): Instance used for Reading Data from API
    """
    exchange_df = r.read_timeinterval(
        start_date=datetime(2024, 4, 1), end_date=datetime.now()
    )
    exchange_df.to_parquet(OUTPUT_FILE)


def fetch_update(r: CurrencyReader) -> None:
    """
    Fetches data and updates curernt version if necessary

    Args:
        r (CurrencyReader): Instance used for Reading Data from API
    """
    now: datetime = datetime.now()
    if now > datetime.fromtimestamp(os.path.getmtime(OUTPUT_FILE)):
        try:
            # fetch current data
            update_dict = r.read(now)
            # append date
            update_dict["Date"] = now
            update_df = pd.DataFrame([update_dict])
            # read parquet file, update and safe again
            df = pd.read_parquet(OUTPUT_FILE)
            df = pd.concat([update_df, df], ignore_index=True)
            df.to_parquet(OUTPUT_FILE)
        except Exception:
            print(f"No Data found for date {now}")


def fetch_daily(r: CurrencyReader) -> None:
    """
    Fetches data daily and updates curernt version

    Args:
        r (CurrencyReader): Instance used for Reading Data from API
    """

    while True:
        fetch_update(r)
        visualize()
        time.sleep(CHECKINTERVALL)


def visualize():
    v = Visualizer(OUTPUT_FILE)
    v.read_fom_parquet()
    fig = v.create_scatter_plot()
    fig.show()


if __name__ == "__main__":
    r = CurrencyReader(START_CURRENCY, CURRENCIES)
    initial_fetch_exchange(r)
    visualize()
