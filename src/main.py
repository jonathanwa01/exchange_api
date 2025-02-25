from datetime import datetime
from modules.reader import CurrencyReader
from modules.visualizer import Visualizer

CHECKINTERVALL = 24 * 60 * 60
OUTPUT_FOLDER = "data/"
CURRENCIES: list[str] = [
    "Australian Dollar",
    "US Dollar",
    "Israeli Shekel",
    "Cuban Peso",
    "Japanese Yen",
]


def update_exchange() -> None:
    r = CurrencyReader("Euro", CURRENCIES)
    exchange_df = r.read_timeinterval(
        start_date=datetime(2024, 4, 1), end_date=datetime.now()
    )
    exchange_df.to_parquet(OUTPUT_FOLDER + "exchange.parquet")


if __name__ == "__main__":
    update_exchange()
    v = Visualizer(OUTPUT_FOLDER + "exchange.parquet")
    v.read_fom_parquet()
    fig = v.create_scatter_plot()
    fig.show()
