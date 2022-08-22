import requests
from bs4 import BeautifulSoup
import json

URL = "https://quotes.toscrape.com/"

empty_results_flag = False
i = 1

results = []
# [
#   {
#       "quote": "bla bla",
#       "author": "Albert Einstein",
#       "tags": ["books", "mind"]
#   }
# ]

while not empty_results_flag and i <= 100:
    print(i)

    page_url = URL + "page/" + str(i)
    # print(page_url)

    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")

    quotes = soup.findAll("div", class_="quote")
    # print(quotes)

    if len(quotes) == 0:
        empty_results_flag = True
        continue

    for quote in quotes:
        text = quote.find("span", class_="text").text
        # print(text)

        author = quote.find("small", class_="author").text
        # print(author)

        tags = [x.text for x in quote.findAll("a", class_="tag")]
        # print(tags)

        results.append({"quote": text, "author": author, "tags": tags})

    i += 1


with open("utilities/results.json", "w") as f:
    json.dump(results, f)
