import pytest
from unittest.mock import patch
from src.utils import sort_by_period, greet_user, read_from_xlsx, get_top_transactions
import datetime

@pytest.mark.parametrize(
    "my_list, date, period",
    [
        ([], "2025-02-11 21:27:36", "W"),
        ([], "2025-02-11 21:27:36", "M"),
        ([], "2025-02-11 21:27:36", "Y"),
        ([], "2025-02-11 21:27:36", "ALL"),
    ],
)
def test_sort_by_period_empty(my_list, date, period):
    assert sort_by_period(my_list, date, period).to_dict() == {}


def test_sort_by_period(short_list_of_transactions):
    assert sort_by_period(short_list_of_transactions, "2020-12-11 21:27:36").to_dict(orient="records") == [
        {
            "Дата операции": "08.12.2020 21:29:43",
            "Дата платежа": "08.12.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -364.49,
            "Валюта операции": "RUB",
            "Сумма платежа": -364.49,
            "Валюта платежа": "RUB",
            "Кэшбэк": 30,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Дикси",
            "Бонусы (включая кэшбэк)": 7,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 364.49,
        }
    ]


@patch("datetime.datetime")
def test_greet_user(mock_now):
    mock_now.now.return_value = datetime.datetime.strptime("2025-12-31 21:23:23", "%Y-%m-%d %H:%M:%S")
    time_1 = greet_user(None)
    assert time_1 == "Доброй ночи!"


@patch("pandas.read_excel")
def test_read_from_xlsx(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = []
    list_1 = read_from_xlsx("test")
    assert list_1 == []


@patch("pandas.read_excel")
def test_read_from_xlsx_1(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = [{
            "Дата операции": "08.12.2020 21:29:43",
            "Дата платежа": "08.12.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -364.49,
            "Валюта операции": "RUB",
            "Сумма платежа": -364.49,
            "Валюта платежа": "RUB",
            "Кэшбэк": 30,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Дикси",
            "Бонусы (включая кэшбэк)": 7,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 364.49,
        }]
    list_1 = read_from_xlsx("test")
    assert list_1 == [{
            "Дата операции": "08.12.2020 21:29:43",
            "Дата платежа": "08.12.2020",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -364.49,
            "Валюта операции": "RUB",
            "Сумма платежа": -364.49,
            "Валюта платежа": "RUB",
            "Кэшбэк": 30,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Дикси",
            "Бонусы (включая кэшбэк)": 7,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 364.49,
        }]


@patch("pandas.DataFrame")
def test_get_top_transactions(mock_top_transactions):
    mock_top_transactions.return_value.sort_values.return_value = []
    transactions_1 = get_top_transactions("test")
    assert transactions_1 == []


# @patch("pandas.DataFrame")
# def test_get_top_transactions_1(mock_top_transactions):
#     mock_top_transactions.return_value.loc.return_value.sort_values.return_value = [{
#             "Дата платежа": "08.12.2020",
#             "Сумма операции": 364,
#             "Категория": "Супермаркеты",
#             "Описание": "Дикси"
#         }]
#     transactions_1 = get_top_transactions("test")
#     assert transactions_1 == [{
#             "Дата платежа": "08.12.2020",
#             "Сумма операции": 364,
#             "Категория": "Супермаркеты",
#             "Описание": "Дикси"
#         }]
