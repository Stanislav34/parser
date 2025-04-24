import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL для поиска товаров
url = "https://www.21vek.by/search/"

# Список товаров для поиска
queries = ["Lg-26", "Lg-54", "LG-31", "LG-15", "On-54", "On-26", "LY-31", "LY-26", "K-24"]

# Список для хранения данных
all_products = []

for query in queries:
    print(f"Поиск товаров по запросу: {query}")
    
    # Параметры запроса
    params = {
        "term": query,
        "searchId": "1745493655216049",  # Пример searchId (можно генерировать случайно)
        "category_id": "251"  # Фильтр по категории (например, смесители)
    }
    
    # Заголовки (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://www.21vek.by/"
    }
    
    # Отправляем GET-запрос
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        # Парсим HTML-страницу
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Ищем товары
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
        print(f"Ошибка при запросе: {response.status_code}")
        print(f"Ответ сервера: {response.text}")

# Сохраняем данные в Excel
if all_products:
    df = pd.DataFrame(all_products)
    df.to_excel("products.xlsx", index=False)
    print("Данные успешно сохранены в файл.")
else:
    print("Товары не найдены.")