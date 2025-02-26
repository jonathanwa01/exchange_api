import threading
from main import CURRENCIES, START_CURRENCY, fetch_daily, initial_fetch_exchange
from modules.reader import CurrencyReader


if __name__ == "__main__":
    r = CurrencyReader(START_CURRENCY, CURRENCIES)
    initial_fetch_exchange(r)
    thread = threading.Thread(target=fetch_daily, args=(r,), name="DailyFetchThread")
    thread.start()
