import requests
import logging
import time
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Заголовки для имитации запроса от браузера
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64)",
    "x-onliner-client": "type=web; version=1.0.0; application=catalog",
}

# Базовый URL для поиска товаров
BASE_URL = "https://catalog.onliner.by/sdapi/catalog.api/search/products"

def normalize(text):
    """Нормализация строки: нижний регистр, удаление лишних символов."""
    return text.lower().replace("-", " ").strip()

def parse_onliner_catalog(queries, max_pages=2):
    products = []

    # Создаем список нормализованных шаблонов с границами слов и обязательными окончаниями
    patterns = [re.compile(rf"\b{re.escape(normalize(q))}\b(?!\d)") for q in queries]  # исключаем, если после идет цифра

    for query in queries:
        logger.info(f"🔍 Поиск товаров на Onliner.by по запросу: {query}")
        page = 1

        while page <= max_pages:
            params = {
                "query": query,
                "page": page,
                "limit": 30
            }

            try:
                response = requests.get(BASE_URL, headers=HEADERS, params=params)
                response.raise_for_status()
                data = response.json()

                items = data.get("products", [])
                if not items:
                    logger.info(f"На странице {page} нет товаров для запроса '{query}'. Переход к следующему.")
                    break

                for item in items:
                    name = item.get("full_name") or item.get("name") or ""
                    norm_name = normalize(name)

                    # Строгая фильтрация по регулярным шаблонам
                    if not any(pattern.search(norm_name) for pattern in patterns):
                        continue

                    # Дополнительная фильтрация: исключаем товары с неприемлемыми словами или абстрактными моделями
                    if re.search(r"\bby\b|\bis-\b|dz\b", norm_name):
                        logger.info(f"Исключен товар с неприемлемым названием: {name}")
                        continue

                    price_info = item.get("prices", {})
                    if price_info and isinstance(price_info, dict) and "price_min" in price_info:
                        price_amount = price_info["price_min"].get("amount", "Нет в наличии")
                        price_currency = price_info["price_min"].get("currency", "BYN")
                        price = f"{price_amount} {price_currency}"
                    else:
                        price = "Нет в наличии"

                    products.append({
                        "name": name,
                        "price": price,
                        "website": "onliner.by"
                    })

                logger.info(f"Обработана страница {page} для запроса '{query}'. Найдено товаров: {len(items)}")
                page += 1
                time.sleep(0.3)

            except Exception as e:
                logger.error(f"Ошибка при запросе данных с Onliner.by: {e}")
                break

    return products
