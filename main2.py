import logging
import pandas as pd
from parser_21vek import parse_21vek
from parser_gemma import parse_gemma
from parser_catalog_onliner import parse_onliner_catalog
from parser_oma import parse_oma
from parser_ksk import parse_ksk
from parser_mile import parse_mile  # Импортируем новый парсер

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def normalize_products(products, name_key, price_key, site_key):
    """Приведение структуры данных к общему формату."""
    return [
        {
            "name": product[name_key],
            "price": product[price_key],
            "website": product[site_key]
        }
        for product in products
    ]

def main():
    queries = ["Lg-26", "Lg-54", "LG-31", "LG-15", "On-54", "On-26", "LY-31", "LY-26", "K-24", "Смеситель K24"]
    
    # Парсинг 21vek.by
    logger.info("Запускаем парсинг с 21vek.by...")
    try:
        raw_21vek = parse_21vek(queries)
        products_21vek = normalize_products(raw_21vek, "Наименование товара", "Цена товара", "Сайт")
        logger.info(f"Найдено {len(products_21vek)} товаров на 21vek.by")
    except Exception as e:
        logger.error(f"Ошибка при парсинге 21vek.by: {e}")
        products_21vek = []

    # Парсинг gemma.by
    logger.info("Запускаем парсинг с gemma.by...")
    try:
        raw_gemma = parse_gemma(queries)
        products_gemma = normalize_products(raw_gemma, "Наименование товара", "Цена товара", "Сайт")
        logger.info(f"Найдено {len(products_gemma)} товаров на gemma.by")
    except Exception as e:
        logger.error(f"Ошибка при парсинге gemma.by: {e}")
        products_gemma = []

    # Парсинг Onliner
    logger.info("Запускаем парсинг с Onliner...")
    try:
        products_onliner = parse_onliner_catalog(queries)
        logger.info(f"Найдено {len(products_onliner)} товаров на Onliner")
    except Exception as e:
        logger.error(f"Ошибка при парсинге Onliner: {e}")
        products_onliner = []

    # Парсинг oma.by
    logger.info("Запускаем парсинг с oma.by...")
    try:
        products_oma = parse_oma(queries)
        logger.info(f"Найдено {len(products_oma)} товаров на oma.by")
    except Exception as e:
        logger.error(f"Ошибка при парсинге oma.by: {e}")
        products_oma = []

    # Парсинг ksk.by
    logger.info("Запускаем парсинг с ksk.by...")
    try:
        raw_ksk = parse_ksk(queries)
        products_ksk = normalize_products(raw_ksk, "name", "price", "website")
        logger.info(f"Найдено {len(products_ksk)} товаров на ksk.by")
    except Exception as e:
        logger.error(f"Ошибка при парсинге ksk.by: {e}")
        products_ksk = []

    # Парсинг mile.by
    logger.info("Запускаем парсинг с mile.by...")
    try:
        raw_mile = parse_mile(queries)
        products_mile = normalize_products(raw_mile, "name", "price", "website")
        logger.info(f"Найдено {len(products_mile)} товаров на mile.by")
    except Exception as e:
        logger.error(f"Ошибка при парсинге mile.by: {e}")
        products_mile = []

    # Собираем все товары
    all_products = products_21vek + products_gemma + products_onliner + products_oma + products_ksk + products_mile

    if all_products:
        df = pd.DataFrame(all_products, columns=["name", "price", "website"])  # фиксированные колонки
        df.to_excel("products.xlsx", index=False)
        logger.info(f"Данные сохранены в файл products.xlsx. Всего товаров: {len(all_products)}")
    else:
        logger.warning("Нет найденных товаров для сохранения.")

if __name__ == "__main__":
    main()
