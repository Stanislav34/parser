from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Используем ChromeDriverManager для автоматической загрузки драйвера
service = Service(ChromeDriverManager().install())

# Запуск браузера
driver = webdriver.Chrome(service=service)

# Открытие страницы
driver.get("https://diy.by/grodno/")

# Даем время для загрузки страницы
time.sleep(10)

# Попробуем найти кнопку для cookies
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cookie-notification__control")))
    print("Кнопка для куки найдена")
    accept_cookies_button.click()
except Exception as e:
    print(f"Ошибка при поиске кнопки с куками: {e}")
    driver.save_screenshot("error_screenshot.png")  # Делаем снимок экрана, если ошибка
    driver.quit()
    exit()

# Даем время на переход, если это нужно
time.sleep(15)

# Проверим, что страница загрузилась и поле поиска доступно
try:
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ID1380808054")))
    print("Поле для поиска найдено")
    search_box.click()
except Exception as e:
    print(f"Ошибка при поиске поля ввода: {e}")
    driver.save_screenshot("error_screenshot_search.png")  # Делаем снимок экрана, если ошибка
    driver.quit()
    exit()

# Вводим запрос в поле поиска
search_box.send_keys("сантехника")

# Даем время, чтобы результаты поиска появились
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'search-card__title')]")))

# Считываем найденные товары
products = driver.find_elements(By.XPATH, "//a[contains(@class, 'search-card__title')]")
prices = driver.find_elements(By.XPATH, "//span[contains(@class, 'product-price__price-current-main')]")

# Выводим найденные товары и цены
for product, price in zip(products, prices):
    print(f"Название: {product.text}, Цена: {price.text}")

# Закрываем браузер
driver.quit()
