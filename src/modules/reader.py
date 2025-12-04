from datetime import datetime, timedelta
import pandas as pd
import requests
from tqdm import tqdm


class CurrencyReader:
    """
    A class which handles the request and reading of the exchange api

    Attr:
        URL (str): URL to exhange API
    """

    URL_STRUCTURE_EXCHANGE = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{start_currency}.json"

    def __init__(self, start_currency: str, currencies: list[str]):
        """
        Constructor. Creates a reader instance to read from API.

        Args:
            start_currency (str): currency to be converted
            currencies (list): list of currencies to be read out from the api

        """
        self.abbreviation_parser = AbbreviationParser()
        self.start_currency: str = start_currency
        self.currencies: list[str] = currencies

    def read(self, date: datetime) -> dict[str, float]:
        """
        Requests exchange rates on a given date.

        Args:
            date (datetime): date on which the data is fetched

        Returns:
            exchange_dict (dict[str, float]): Dictionary of exchange rates
            relative to self.start_currency

        Exceptions:
            Exception: Invalid Currency
        """
        start_currency_abbrv: str = self.abbreviation_parser.name_to_abbrv(
            self.start_currency
        )
        exchange_currencies: list[str] = [
            self.abbreviation_parser.name_to_abbrv(name) for name in self.currencies
        ]

        exchange_dict: dict[str, float] = {}
        response = requests.get(
            CurrencyReader.URL_STRUCTURE_EXCHANGE.format(
                date=date.strftime("%Y-%m-%d"),
                apiVersion="v1",
                start_currency=start_currency_abbrv,
            )
        )

        if response.status_code == 200:
            response_data = response.json()
            for cur in exchange_currencies:
                if cur in response_data[start_currency_abbrv]:
                    exchange_dict[self.abbreviation_parser.abbrv_to_name(cur)] = (
                        response_data[start_currency_abbrv][cur]
                    )
                else:
                    raise Exception(f"Currency code {cur} is invalid")
        elif response.status_code == 404:
            raise FileNotFoundError(
                f"Page {
                    CurrencyReader.URL_STRUCTURE_EXCHANGE.format(
                        date=date,
                        apiVersion='v1',
                        start_currency=start_currency_abbrv)} could not be found"
            )

        return exchange_dict

    def read_timeinterval(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Requests exchange rates in a given time interval between start_date
        and end_date

        Args:
            start_date (datetime): start date
            end_date (datetime): end date

        Returns:
            exchange_df (pd.DataFrame): dataframe of exchange rates
            relative to self.start_currency
        """

        exchange_df: pd.DataFrame = pd.DataFrame(columns=["Date"] + self.currencies)
        time_dif: timedelta = end_date - start_date
        print("Fetching Exchange Data from API")
        for _ in tqdm(range(time_dif.days)):
            exchange_dict = self.read(date=start_date)
            df = pd.DataFrame([exchange_dict])
            df["Date"] = pd.to_datetime(start_date)
            exchange_df = pd.concat([exchange_df, df], ignore_index=True)
            start_date += timedelta(days=1)
        return exchange_df


class AbbreviationParser:
    """
    A class that handles the translation of abbreviations into name and vice versa
    """

    URL_STRUCTURE_CURRENCY_LIST = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/{endpoint}"

    def __init__(self):
        """
        Constructor.

        """
        response = requests.get(
            AbbreviationParser.URL_STRUCTURE_CURRENCY_LIST.format(
                date="latest", apiVersion="v1", endpoint="currencies.json"
            )
        )
        self.abbreviation_dict: dict[str, str] = (
            response.json() if response.status_code == 200 else {}
        )

    def abbrv_to_name(self, abbrv: str) -> str:
        """
        Returns full name of the abbreviation

        Args:
            abbrv (str): String of abbreviation

        Returns:
            full_name (str): String of full name
        """
        if abbrv in self.abbreviation_dict:
            return self.abbreviation_dict[abbrv]
        else:
            raise Exception(f"Abbreviation code {abbrv} is invalid")

    def name_to_abbrv(self, name: str) -> str:
        """
        Returns full name of the abbreviation

        Args:
            abbrv (str): String of abbreviation

        Returns:
            full_name (str): String of full name
        """
        for key in self.abbreviation_dict:
            if self.abbreviation_dict[key] == name:
                return key
        raise Exception(f"Currency name {name} is invalid")
