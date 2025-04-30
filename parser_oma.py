import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.oma.by/search/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def normalize_query(query):
    """Нормализуем запрос, чтобы сделать его сравнимым с названием товара."""
    return query.lower().replace("-", " ")

def filter_product(name, queries):
    """Фильтруем товар по списку запросов."""
    name_normalized = normalize_query(name)
    
    for query in queries:
        query_normalized = normalize_query(query)
        
        if query_normalized in name_normalized:
            return True
    return False

def parse_oma(queries):
    products = []
    
    for query in queries:
        print(f"🔍 Поиск товаров на OMA.by по запросу: {query}")
        params = {
            "SORTBY": "RELEVANSE",
            "TAB": "catalog",
            "q": query
        }
        
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем все товары на странице
        product_items = soup.select('.product-item')
        
        if not product_items:
            print(f"На странице нет товаров для запроса '{query}'.")
            continue
        
        for item in product_items:
            # Извлекаем название товара
            name = item.select_one('.product-item_title .wrapper').text.strip()

            # Проверяем, что товар подходит под фильтрацию
            if not filter_product(name, queries):
                continue  # Пропускаем товар, если он не подходит
            
            # Извлекаем цену товара
            price_element = item.select_one('.product-price-block .price__normal')
            price = price_element.text.strip() if price_element else "Цена не указана"
            
            products.append({
                "name": name,
                "price": price,
                "website": "oma.by"
            })

    return products
