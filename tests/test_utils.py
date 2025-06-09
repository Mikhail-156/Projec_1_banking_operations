import pytest

from src.utils import sort_by_period, greet_user


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