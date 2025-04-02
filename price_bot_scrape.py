import requests
from bs4 import BeautifulSoup
import re
import time
import random

# Rotate User-Agents to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Headers to mimic a browser request
def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

# Fetch price from Amazon
def fetch_amazon_price(product_name):
    url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.select_one("span.a-price > span.a-offscreen")
        if price_tag:
            price_text = re.search(r"[\d,]+\.?\d*", price_tag.text).group()
            return float(price_text.replace(",", ""))
        print("Amazon: No price found in HTML.")
        return None
    except Exception as e:
        print(f"Amazon Error: {e}")
        return None

# Fetch price from eBay
def fetch_ebay_price(product_name):
    url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.select_one("span.s-item__price")
        if price_tag:
            price_text = re.search(r"[\d,]+\.?\d*", price_tag.text).group()
            return float(price_text.replace(",", ""))
        print("eBay: No price found in HTML.")
        return None
    except Exception as e:
        print(f"eBay Error: {e}")
        return None

# Fetch price from Walmart
def fetch_walmart_price(product_name):
    url = f"https://www.walmart.com/search?q={product_name.replace(' ', '+')}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.select_one("div[data-automation-id='product-price'] span")
        if price_tag:
            price_text = re.search(r"[\d,]+\.?\d*", price_tag.text).group()
            return float(price_text.replace(",", ""))
        print("Walmart: No price found in HTML.")
        return None
    except Exception as e:
        print(f"Walmart Error: {e}")
        return None

# Compare prices across platforms
def compare_prices(product_name):
    prices = {}
    prices["Amazon"] = fetch_amazon_price(product_name)
    time.sleep(5)  # Increased delay
    prices["eBay"] = fetch_ebay_price(product_name)
    time.sleep(5)
    prices["Walmart"] = fetch_walmart_price(product_name)
    # Filter out None values and sort by price
    valid_prices = {k: v for k, v in prices.items() if v is not None}
    return sorted(valid_prices.items(), key=lambda x: x[1]) if valid_prices else []

# Personalized comparison with budget filter
def personalized_comparison(product_name, max_budget):
    prices = compare_prices(product_name)
    if not prices:
        return "No price data available."
    filtered_prices = [(platform, price) for platform, price in prices if price <= max_budget]
    return filtered_prices if filtered_prices else "No options found within your budget."

# Main function to run the bot
def run_price_bot():
    print("Welcome to the Web Scraping Price Comparison Bot!")
    product_name = input("Enter the product name to compare: ")
    try:
        max_budget = float(input("Enter your maximum budget (in USD): "))
    except ValueError:
        print("Invalid budget. Using default of $500.")
        max_budget = 500.0
    
    # Get and display results
    result = personalized_comparison(product_name, max_budget)
    print("\nPrice Comparison Results:")
    if isinstance(result, str):
        print(result)
    else:
        for platform, price in result:
            print(f"{platform}: ${price:.2f}")

# Run the bot
if __name__ == "__main__":
    run_price_bot()