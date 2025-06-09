import os
from unittest.mock import patch

from dotenv import load_dotenv

from src.api_search import get_currency_rate, get_stock_exchange

load_dotenv()
API_KEY = os.getenv("API_KEY")


@patch("requests.get")
def test_get_currency_rate(mock_get):
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Value": 100.00}}}
    assert get_currency_rate(["USD"]) == [{"currency": "USD", "rate": 100.00}]

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    mock_get.assert_called_once_with(url)


@patch("requests.get")
def test_get_stock_exchange(mock_get):
    mock_get.return_value.json.return_value = {"data": [{"symbol": "AAPL", "open": 100.00}]}
    assert get_stock_exchange(["AAPL"]) == [{"stock": "AAPL", "price": 100.00}]

    url = f"http://api.marketstack.com/v2/eod?access_key={API_KEY}&symbols=AAPL"
    mock_get.assert_called_once_with(url)