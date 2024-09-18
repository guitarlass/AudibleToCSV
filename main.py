import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.audible.com/search?keywords=colin+morgan")
content = response.text
soup = BeautifulSoup(content, "html.parser")

productList = []
products = soup.select(".productListItem")
for product in products:
    title = product.select_one(".bc-heading .bc-link").get_text(strip=True)
    buyBox = product.select(".adblBuyBoxPrice p span")
    price = buyBox[1].get_text(strip=True).replace("$", "") if buyBox else ''
    # price = buyBox[1].get_text(strip=True)
    #
    productList.append({"title": title, "price" : price})

print(productList)
