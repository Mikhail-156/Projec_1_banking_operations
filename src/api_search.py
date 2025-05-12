import logging
import os

import requests
from dotenv import load_dotenv

log_path = "../logs/api_search.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("api_search")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_currency_rate(currencies: list[str]) -> list[dict]:
    """Возвращает курс валют в рублях."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    answer: list = []
    try:
        response = requests.get(url).json()
        for currency in currencies:
            answer.append({"currency": currency, "rate": response["Valute"][currency]["Value"]})
        logger.info("Успешно получен ответ на API-запрос")
    except Exception as e:
        logger.critical(f"API-запрос неуспешен. Возможная причина: {e}")
    return answer


def get_stock_exchange(stocks: list[str], usd_rate: float = 1) -> list[dict]:
    """Возвращает стоимость акций в долларах. Чтобы вернуть стоимость в другой валюте,
    необходимо присвоить курс доллара необязательному параметру usd_rate."""
    stocks_str = ",".join(stocks)
    url = f"http://api.marketstack.com/v2/eod?access_key={API_KEY}&symbols={stocks_str}"
    answer = []
    try:
        response = requests.get(url).json()
        for i in range(len(stocks)):
            answer.append(
                {
                    "stock": response["data"][i]["symbol"],
                    "price": round(response["data"][i]["open"] * usd_rate, 2),
                }
            )
        logger.info("Успешно получен ответ на API-запрос")
    except Exception as e:
        logger.critical(f"API-запрос неуспешен. Возможная причина: {e}")
    return answer
