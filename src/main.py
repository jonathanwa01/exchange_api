from datetime import datetime
from modules.reader import CurrencyReader
from modules.visualizer import Visualizer

OUTPUT_FOLDER = "data/"

if __name__ == "__main__":
    currencies: list[str] = [
        "Australian Dollar",
        "US Dollar",
        "Israeli Shekel",
        "Cuban Peso",
        "Japanese Yen",
    ]
    r = CurrencyReader("Euro", currencies)
    exchange_df = r.read_timeinterval(
        start_date=datetime(2024, 4, 1),
        end_date=datetime(2024, 7, 1))
    print(exchange_df)
    exchange_df.to_parquet(OUTPUT_FOLDER + "output.parquet")

    v = Visualizer(OUTPUT_FOLDER + "output.parquet")
    v.read_fom_parquet()
    fig = v.create_scatter_plot()
    fig.show()
