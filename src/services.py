import logging
import os

log_path = "../logs/services.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("services")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def simple_search(transactions_list: list[dict], search_info: str) -> list[dict]:
    """Функция принимает список словарей с данными о транзакциях и строку поиска,
    а возвращает список тех транзакций, в описании или категории которых есть строка поиска."""
    filtered_transactions = []
    for transaction in transactions_list:
        try:
            # Определяет, где искать
            if transaction.get("Категория"):
                search_in = str(transaction["Категория"]) + transaction["Описание"]
            else:
                search_in = transaction["Описание"]
            if search_info.lower() in search_in.lower():
                filtered_transactions.append(transaction)
        except KeyError as e:
            logger.warning(f"Передана транзакция без необходимого ключа: {e}")
            continue
    logger.info(f"Получено {len(filtered_transactions)} транзакций из {len(transactions_list)}.")
    return filtered_transactions
