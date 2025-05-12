import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_mile(queries):
    base_url = "https://mile.by/search/?q="
    all_products = []

    for query in queries:
        search_query = query.replace("-", " ")  # Заменяем дефисы на пробелы
        logger.info(f"🔍 Поиск товаров на mile.by по запросу: {search_query}")

        url = base_url + search_query.replace(" ", "+")
        logger.info(f"Формируем URL: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            logger.warning(f"Не удалось загрузить страницу по запросу '{query}'")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.find_all('div', class_='anons-name')

        if not product_elements:
            logger.warning(f"Не найдено товаров по запросу '{query}'")
            continue

        # Создаем паттерн для фильтрации
        # Например: query = "LG-26" → паттерн: r"\bLG[-\s]?26([A-Z]*)?\b"
        brand, model = query.split("-")
        pattern = re.compile(rf"\b{re.escape(brand)}[-\s]?{re.escape(model)}([A-Z]{{0,2}})?\b", re.IGNORECASE)

        for product in product_elements:
            name_tag = product.find('a', href=True)
            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)

            # Применяем фильтрацию с помощью регулярного выражения
            if not pattern.search(name):
                continue  # Пропускаем, если не совпадает с паттерном

            product_url = "https://mile.by" + name_tag['href']  # Формируем полный URL товара

            # Извлекаем цену
            price_tag = product.find_next('p', class_='price')
            if price_tag:
                price = price_tag.find('span').get_text(strip=True) if price_tag.find('span') else "Цена не указана"
            else:
                price = "Цена не указана"

            all_products.append({
                'name': name,
                'price': price,
                'product_url': product_url,
                'website': 'mile.by'
            })

        logger.info(f"✅ Найдено {len(all_products)} подходящих товаров на mile.by по запросу '{query}'")

    return all_products

# Пример использования
queries = ["Lg-26", "Lg-54", "LG-31", "LG-15", "On-54", "On-26", "LY-31", "LY-26", "K-24"]
products_mile = parse_mile(queries)
logger.info(f"Общее количество товаров на mile.by: {len(products_mile)}")
