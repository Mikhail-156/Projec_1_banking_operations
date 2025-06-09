import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_empty():
    assert spending_by_category(pd.DataFrame([]), "category").to_dict(orient="records") == []


def test_spending_by_category(short_list_of_transactions):
    assert spending_by_category(
        pd.DataFrame(short_list_of_transactions), "различные товары", "2019-02-08 12:41:24"
    ).to_dict(orient="records") == [{"Различные товары": 1004.9}]
