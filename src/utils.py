import datetime
import logging
import os
import re
from datetime import datetime
import pandas as pd
from typing import Any
from src.api_search import get_currency_rate, get_stock_exchange

log_path = "../logs/utils.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def greet_user(date_time: Any) -> str:
    """
    Функция принимает строку с date и time (либо жми энтер если в падлу)
    после выводит приветствие в зависимости от чего вы вели .
    """
    if date_time is None:
        date_time = datetime.now()
    else:
        date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_cards_numbers(transactions_list: pd.DataFrame) -> list[dict]:
    """По каждой карте находит последние 4 цифры, общую сумму расходов за текущий (последний) месяц и кешбэк."""
    total_spending = {}
    try:
        transactions_list_sorted = transactions_list.loc[
            (transactions_list["Сумма операции"] < 0)
            & ((transactions_list["Номер карты"]) != "nan")
            & ((transactions_list["Статус"]) == "OK")
        ]
        cards = transactions_list_sorted.groupby("Номер карты")["Сумма операции с округлением"].agg("sum")
        cards_dict = cards.to_dict()
        for number, spending in cards_dict.items():
            total_spending[str(number)[1:]] = round(spending, 2)
        logger.info(f"Обнаружены данные по {len(total_spending)} картам")
        result = []
        for key, value in cards.items():
            if str(key) != "nan":
                result.append(
                    {
                        "last_digits": str(key)[1:],
                        "total_spent": round(value, 2),
                        "cashback": round(value / 100, 2),
                    }
                )

        logger.info(f"Обнаружены данные по {len(result)} картам")
        return result
    except KeyError as e:
        logger.warning(f"Передана транзакция без необходимого ключа: {e}")
    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")
    return []


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Находит информацию по 5 наибольшим транзакциям за текущий (последний) месяц."""
    top_transactions = []
    try:
        sorted_transactions_list = transactions.loc[
            (transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)
        ].sort_values("Сумма операции с округлением", ascending=False, ignore_index=True)
        for index, transaction in sorted_transactions_list.iterrows():
            if int(index) < 5:
                top_transactions.append(
                    {
                        "date": transaction["Дата платежа"],
                        "amount": transaction["Сумма операции с округлением"],
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
            else:
                break
    except KeyError as e:
        logger.warning(f"Передана транзакция без необходимого ключа: {e}")
    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")
    logger.info(f"Обнаружены топ {len(top_transactions)} транз.")
    return top_transactions


def main_page_func(
    date: str, transactions_list: pd.DataFrame, currencies: list[str], stocks: list[str], usd_rate: float = 1
) -> dict:
    """Основная функция страницы "Главная"."""
    result = {
        "greeting": greet_user(date),
        "cards": get_cards_numbers(transactions_list),
        "top_transactions": get_top_transactions(transactions_list),
        "currency_rates": get_currency_rate(currencies),
        "stock_prices": get_stock_exchange(stocks, usd_rate),
    }
    return result


def read_from_xlsx(xlsx_file: str) -> list[dict]:
    """Читает XLSX-файл file_name с транзакциями и возвращает их в виде списка словарей."""
    try:
        data = pd.read_excel(xlsx_file)
        transactions_list = data.to_dict(orient="records")
        return transactions_list
    except Exception as e:
        logger.critical(f"Произошла ошибка при чтении XLSX-файла: {e}")
        return []


def sort_by_period(
    transactions_list: list[dict], date: str, status: str = "OK", period: str = "M"
) -> pd.core.frame.DataFrame:
    """Из списка всех операций возвращает только операции за текущий период
    (неделя, месяц, год или за всё время). По умолчанию - месяц.
    Если таких нет, то возвращает пустой список."""
    current_period = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%m.%Y-%W")
    current_period_transactions = []
    string_period = ""  # period = "ALL"
    if period == "W":
        string_period = current_period[3:]  # "YYYY-WW"
    elif period == "M":
        string_period = current_period[:7]  # "mm.YYYY"
    elif period == "Y":
        string_period = current_period[3:7]  # "YYYY"
    if len(transactions_list) != 0:
        try:
            if any(
                string_period
                in datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y-%W")
                for x in transactions_list
            ):
                for transaction in transactions_list:
                    transaction_date = datetime.strptime(
                        str(transaction["Дата операции"]), "%d.%m.%Y %H:%M:%S"
                    ).strftime("%m.%Y-%W")
                    if re.search(string_period, transaction_date) and transaction["Статус"] == status:
                        current_period_transactions.append(transaction)
                logger.info(f"Найдено {len(current_period_transactions)} транзакций за переданный период")
            else:
                logger.info(f"Не найдено транзакций для {date}")
                return pd.DataFrame([])
        except KeyError as e:
            logger.critical(f"Передана транзакция без необходимого ключа: {e}")
    return pd.DataFrame(current_period_transactions)
