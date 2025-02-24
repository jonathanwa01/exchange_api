

from datetime import datetime
import pandas as pd
from modules.reader import CurrencyReader

OUTPUT_FOLDER = 'data/'

if __name__ == "__main__":
    currencies: list[str] = ['Australian Dollar', 'US Dollar', 'Israeli Shekel', 'Cuban Peso', 'Japanese Yen']
    r = CurrencyReader('Euro', currencies)
    exchange_df: pd.DataFrame = pd.DataFrame(columns=['Date'] + currencies)
    for year in range(2002,2025):
        date: datetime = datetime(2024, 3,6)
        try:
            exchange_dict = r.read(date.strftime('%Y-%m-%d'))
            exchange_dict['Date'] = year
            df = pd.DataFrame([exchange_dict])
            exchange_df = pd.concat([exchange_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
    exchange_df.to_parquet(OUTPUT_FOLDER + 'output.parquet')

