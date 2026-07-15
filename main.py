import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_books(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching data from: {url}...")

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to retrieve data: {exc}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    data_list = []

    for product in products:
        name_tag = product.h3.a
        name = name_tag.get("title") or name_tag.get_text(strip=True)

        price_tag = product.find("p", class_="price_color")
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        rating_tag = product.find("p", class_="star-rating")
        rating = "No Rating"
        if rating_tag:
            rating_classes = rating_tag.get("class", [])
            rating = rating_classes[1] if len(rating_classes) > 1 else "No Rating"

        data_list.append({"Name": name, "Price": price, "Rating": rating})

    if not data_list:
        print("No product data was found on the page.")
        return

    output_file = "products.csv"
    df = pd.DataFrame(data_list)
    df.to_csv(output_file, index=False)

    print(f"\n🎉 Success! Extracted {len(data_list)} products and saved to '{output_file}'.")
    print(df.head())


if __name__ == "__main__":
    target_url = "https://books.toscrape.com/"
    scrape_books(target_url)