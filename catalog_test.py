import requests
from bs4 import BeautifulSoup

url = "https://catalog.onliner.by/faucet/esko/eskok24"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Ищем тег <a> с нужным классом, в котором содержится цена
price_tag = soup.find("a", class_="offers-description__link_nodecor")

if price_tag:
    price = price_tag.text.strip()
    print("Цена найдена:", price)
else:
    print("Цена не найдена.")
