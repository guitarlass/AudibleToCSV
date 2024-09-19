import requests
from bs4 import BeautifulSoup
import csv

response = requests.get("https://www.audible.com/search?keywords=colin+morgan&pageSize=50")
content = response.text
soup = BeautifulSoup(content, "html.parser")

productList = []
products = soup.select(".productListItem")
for product in products:

    narratorList = []
    narrators = product.select(".narratorLabel span a")
    for narrator in narrators:
        if narrator:
            narratorList.append(narrator.get_text().strip())

    if "Colin Morgan" in narratorList:
        title = product.select_one(".bc-heading .bc-link").get_text(strip=True)

        subdes = product.select_one(".subtitle span")
        subtitle = subdes.get_text(strip=True) if subdes else ''

        author_obj = product.select_one(".authorLabel span a")
        author = author_obj.get_text(strip=True) if author_obj else ''

        duration_obj = product.select_one(".runtimeLabel span")
        duration = duration_obj.get_text(strip=True).replace("Length: ", "") if duration_obj else ''

        release_date_obj = product.select_one(".releaseDateLabel span")
        release_date = release_date_obj.get_text(strip=True).replace("Release date:", "").strip() if release_date_obj else ''

        language_obj = product.select_one(".languageLabel span")
        language = language_obj.get_text(strip=True).replace("Language:", "").strip() if language_obj else ''



        rating_obj = product.select_one(".ratingsLabel .bc-pub-offscreen")
        rating = rating_obj.get_text(strip=True) if rating_obj else ''

        buyBox = product.select(".adblBuyBoxPrice p span")
        price = buyBox[1].get_text(strip=True).replace("$", "") if buyBox else ''
        # price = buyBox[1].get_text(strip=True)
        #
        productList.append({"title": title, "subtitle": subtitle, "author": author, "duration": duration, "price": price,
                            "release_date": release_date, "language": language, "rating": rating, "narrators": narratorList})

headers = ["title", "subtitle", "author", "duration", "price", "release_date", "language", "rating", "narrators"]

# write to csv
with open("products.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    # write headers
    writer.writeheader()

    for product in productList:
        product["narrators"] = ', '.join(product["narrators"])
        writer.writerow(product)

print("Data has been written to products.csv")