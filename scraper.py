import requests
from bs4 import BeautifulSoup
import csv

print("📄 Starting web scraping of all pages...")

# Base URL
base_url = "http://books.toscrape.com/catalogue/"
start_url = "http://books.toscrape.com/catalogue/page-1.html"

# Open CSV file
with open("books_scraped.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Availability", "Rating"])

    page_num = 1
    while True:
        url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
        print(f"🔍 Scraping {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print("✅ Finished scraping all pages.")
            break
        
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all('article', class_='product_pod')
        
        if not books:
            print("✅ No more books found.")
            break

        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            avail = book.find('p', class_='instock availability').text.strip()
            rating = book.p['class'][1]
            writer.writerow([title, price, avail, rating])
        
        page_num += 1

print("🎉 All books scraped and saved to books_scraped.csv")
