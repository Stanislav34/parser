import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_ksk(queries):
    base_url = "https://ksk.by/search/?search="
    all_products = []

    for query in queries:
        search_query = query.replace("-", " ")
        logger.info(f"🔍 Поиск товаров на KSK.by по запросу: {search_query}")

        url = base_url + search_query.replace(" ", "+")
        logger.info(f"Формируем URL: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            logger.warning(f"Не удалось загрузить страницу по запросу '{query}'")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.find_all('div', class_='squat-description')

        if not product_elements:
            logger.warning(f"Не найдено товаров по запросу '{query}'")
            continue

        # Создаем паттерн для фильтрации
        # Например: query = "LG-26" → паттерн: r"\bLG[-\s]?26([A-Z]*)?\b"
        brand, model = query.split("-")
        pattern = re.compile(rf"\b{re.escape(brand)}[-\s]?{re.escape(model)}([A-Z]{{0,2}})?\b", re.IGNORECASE)

        for product in product_elements:
            name_tag = product.find('div', class_='name')
            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)

            if not pattern.search(name):
                continue  # Пропускаем, если не совпадает с паттерном

            link_tag = name_tag.find('a', href=True)
            product_url = link_tag['href'] if link_tag else "Нет ссылки"

            price_tag = product.find('div', class_='price')
            if price_tag and 'hide_price' not in price_tag.get('class', []):  # Проверка на скрытую цену
                new_price_tag = price_tag.find('span')
                new_price = new_price_tag.get_text(strip=True) if new_price_tag else "Цена не указана"

                old_price_tag = price_tag.find('span', class_='price-cross')
                old_price = old_price_tag.get_text(strip=True) if old_price_tag else "Цена не указана"
            else:
                new_price = old_price = "Цена не указана"  # Если цена скрыта

            all_products.append({
                'name': name,
                'price': new_price,
                'old_price': old_price,
                'product_url': product_url,
                'website': 'ksk.by'
            })

        logger.info(f"✅ Найдено {len(all_products)} подходящих товаров на ksk.by по запросу '{query}'")

    return all_products

# Пример использования
queries = ["Lg-26", "Lg-54", "LG-31", "LG-15", "On-54", "On-26", "LY-31", "LY-26", "K-24"]
products_ksk = parse_ksk(queries)
logger.info(f"Общее количество товаров на KSK.by: {len(products_ksk)}")
