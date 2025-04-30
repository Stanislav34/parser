# import requests
# from bs4 import BeautifulSoup

# def parse_gemma(queries):
#     """
#     Парсер для сайта gemma.by.
    
#     :param queries: Список запросов для поиска товаров.
#     :return: Список словарей с данными о товарах.
#     """
#     # Базовый URL для поиска товаров
#     url = "https://gemma.by/index.php"
    
#     # Список для хранения данных
#     all_products = []
    
#     for query in queries:
#         print(f"Поиск товаров по запросу: {query}")
        
#         # Параметры запроса
#         params = {
#             "route": "product/search",  # Параметр для поиска
#             "search": query             # Запрос для поиска
#         }
        
#         # Заголовки (User-Agent)
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#             "Referer": "https://gemma.by/"
#         }
        
#         # Отправляем GET-запрос
#         response = requests.get(url, params=params, headers=headers)
        
#         if response.status_code == 200:
#             # Парсим HTML-страницу
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Ищем товары
#             products = []
#             for item in soup.select(".product.cloud-style-product"):  # Блок с товарами
#                 try:
#                     # Название товара
#                     name_tag = item.select_one(".product-name")
#                     name = name_tag.text.strip() if name_tag else "Название не указано"
                    
#                     # Фильтрация по ключевому слову
#                     if "смеситель" not in name.lower():
#                         continue  # Пропускаем товары, которые не содержат слово "смеситель"
                    
#                     # Ссылка на товар
#                     link = name_tag["href"] if name_tag and "href" in name_tag.attrs else "#"
                    
#                     # Цена товара
#                     price_tag = item.select_one(".price-reg5")  # Селектор для цены
#                     price = price_tag.text.strip() if price_tag else "Нет в наличии"
                    
#                     products.append({
#                         "Наименование товара": name,
#                         "Цена товара": price,
#                         "Сайт": "gemma.by"
#                     })
#                 except Exception as e:
#                     print(f"Ошибка при парсинге элемента: {e}")
            
#             all_products.extend(products)
#         else:
#             print(f"Ошибка при запросе: {response.status_code}")
#             print(f"Ответ сервера: {response.text}")
    
#     return all_products
import requests
from bs4 import BeautifulSoup
import re

def normalize_name(name):
    return name.lower().replace("-", " ").replace("смеситель", "").strip()

def parse_gemma(queries):
    url = "https://gemma.by/index.php"
    all_products = []
    seen_names = set()

    normalized_queries = [normalize_name(q) for q in queries]

    for query in queries:
        print(f"🔍 Ищу товары по запросу: {query}")
        
        params = {
            "route": "product/search",
            "search": query
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://gemma.by/"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️ Ошибка запроса: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select(".product.cloud-style-product"):
            try:
                name_tag = item.select_one(".product-name")
                price_tag = item.select_one(".price-reg5")

                if not name_tag:
                    continue

                name = name_tag.text.strip()
                norm_name = normalize_name(name)

                # фильтрация: ищем совпадения по нормализованным запросам
                if not any(re.search(rf"\b{re.escape(q)}\b", norm_name) for q in normalized_queries):
                    continue

                # пропускаем дубликаты
                if norm_name in seen_names:
                    print(f"⛔ Дубликат: {name}")
                    continue
                seen_names.add(norm_name)

                price = price_tag.text.strip() if price_tag else "Нет в наличии"

                all_products.append({
                    "Наименование товара": name,
                    "Цена товара": price,
                    "Сайт": "gemma.by"
                })
                print(f"✅ Найден: {name}")

            except Exception as e:
                print(f"Ошибка при парсинге товара: {e}")
    
    return all_products
