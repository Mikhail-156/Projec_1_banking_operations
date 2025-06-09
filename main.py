import datetime
import json
import os

import pandas as pd
from dotenv import load_dotenv

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import read_from_xlsx, main_page_func
from src.views import create_report
from src.utils import sort_by_period


load_dotenv()
OPERATIONS = os.getenv("OPERATIONS")


# Валюта и акции пользователя из user_settings.json
with open("../user_settings.json", "r", encoding="utf-8") as s:
    user_information = json.load(s)
user_currencies = user_information["user_currencies"]
user_stocks = user_information["user_stocks"]

# Получение текущей даты
current_date = datetime.datetime.now()
str_date = datetime.datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")

# Дата, для которой существуют данные в таблице (заменяет данные в строках 28-29, 61-62, 69)
# str_date = "2021-02-09 15:34:23"
# str_month = "02"
# str_year = "2021"
# str_year_month = "2021-02"

# Получение списка транзакций
operations_path = f"../data/{OPERATIONS}.xlsx"
transactions_list = read_from_xlsx(operations_path)

current_month_operations = sort_by_period(transactions_list, str_date)
main_page_data = main_page_func(str_date, current_month_operations, user_currencies, user_stocks)
create_report(main_page_data, "../output/main_page.json")

search_line = "*"
results = simple_search(transactions_list, search_line)
create_report(results, "../output/simple_search.json")

spending_by_category(pd.DataFrame(transactions_list), "Супермаркеты", str_date)
