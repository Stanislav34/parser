import requests
from bs4 import BeautifulSoup

def parse_21vek(queries):
    """
    Парсер для сайта 21vek.by.
    
    :param queries: Список запросов для поиска товаров.
    :return: Список словарей с данными о товарах.
    """
    url = "https://www.21vek.by/search/"
    all_products = []
    
    for query in queries:
        print(f"Поиск товаров по запросу: {query}")
        
        params = {
            "term": query,
            "searchId": "1745493655216049",  # Пример searchId (можно генерировать случайно)
            "category_id": "251"  # Фильтр по категории (например, смесители)
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.21vek.by/"
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            print(f"Успешный ответ для запроса '{query}', начинаем парсить...")
            soup = BeautifulSoup(response.text, "html.parser")
            
            products = []
            for item in soup.select(".style_product__xVGB6"):  # Блок с товарами
                try:
                    name = item.select_one(".CardInfo_info__cUeVj a").text.strip()  # Название товара
                    link = item.select_one(".CardInfo_info__cUeVj a")["href"]  # Ссылка на товар
                    
                    # Цена товара
                    price_tag = item.select_one(".CardPrice_currentPrice__EU_7r")  # Селектор для цены
                    price = price_tag.text.strip() if price_tag else "Нет в наличии"
                    
                    products.append({
                        "Наименование товара": name,
                        "Цена товара": price,
                        "Сайт": "21vek.by"
                    })
                except Exception as e:
                    print(f"Ошибка при парсинге элемента: {e}")
            
            all_products.extend(products)
        else:
            print(f"Ошибка при запросе: {response.status_code} для запроса '{query}'")
            print(f"Ответ сервера: {response.text}")
    
    return all_products
