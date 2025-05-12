from src.services import  simple_search


def test_simple_search_empty():
    assert simple_search([], "") == []


def test_simple_search(short_list_of_transactions):
    assert simple_search(short_list_of_transactions, "анастасия") == [
        {
            "Дата операции": "01.07.2018 12:49:53",
            "Дата платежа": "01.07.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 20,
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Анастасия Л.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        }
    ]


def test_simple_search_no_category():
    assert simple_search([{"Описание": "Анастасия Л."}], "анастасия") == [{"Описание": "Анастасия Л."}]