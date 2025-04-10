import requests
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.table import Table
import re
import time


SCRAPER_API_KEY = "eefa842c395497bc9a8dc046151d9d3b"

console = Console()


def get_scraped_html(url):
    api_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}"
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        console.print(f"[red]Error fetching URL:[/red] {url}\n{e}")
        return None


def extract_price(text):
    match = re.search(r"[\d,]+\.?\d*", text)
    if match:
        return float(match.group().replace(",", ""))
    return None


def fetch_amazon_price(product):
    console.print("[yellow]Searching Amazon...[/yellow]")
    url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"
    html = get_scraped_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        price_tag = soup.select_one("span.a-price > span.a-offscreen")
        if price_tag:
            return extract_price(price_tag.text)
    return None


def fetch_ebay_price(product):
    console.print("[yellow]Searching eBay...[/yellow]")
    url = f"https://www.ebay.com/sch/i.html?_nkw={product.replace(' ', '+')}"
    html = get_scraped_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        price_tag = soup.select_one("span.s-item__price")
        if price_tag:
            return extract_price(price_tag.text)
    return None


def fetch_walmart_price(product):
    console.print("[yellow]Searching Walmart...[/yellow]")
    url = f"https://www.walmart.com/search?q={product.replace(' ', '+')}"
    html = get_scraped_html(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        price_tag = soup.select_one("div[data-automation-id='product-price'] span")
        if price_tag:
            return extract_price(price_tag.text)
    return None


def compare_prices(product, max_budget):
    prices = {
        "Amazon": fetch_amazon_price(product),
        "eBay": fetch_ebay_price(product),
        "Walmart": fetch_walmart_price(product),
    }
    time.sleep(2)
    valid_prices = {k: v for k, v in prices.items() if v is not None}
    filtered = [(site, price) for site, price in valid_prices.items() if price <= max_budget]
    return sorted(filtered, key=lambda x: x[1]) if filtered else []


def display_results(results, product):
    table = Table(title=f"Price Comparison for '{product}'", header_style="bold blue")
    table.add_column("Platform", style="cyan", no_wrap=True)
    table.add_column("Price (USD)", justify="right", style="green")

    for platform, price in results:
        table.add_row(platform, f"${price:.2f}")

    console.print(table)


def run_bot():
    console.print("[bold magenta]💸 Welcome to the API-Powered Price Comparison Bot![/bold magenta]")

    product = console.input("\n[bold]🛍️ Enter product name:[/bold] ")
    try:
        budget = float(console.input("[bold]💰 Enter your max budget ($):[/bold] "))
    except ValueError:
        console.print("[red]Invalid input. Using default budget of $500.[/red]")
        budget = 500.0

    console.print("\n[bold]🔎 Fetching prices... Please wait.[/bold]\n")
    results = compare_prices(product, budget)

    if results:
        display_results(results, product)
    else:
        console.print("[bold red]❌ No options found within your budget.[/bold red]")


if __name__ == "__main__":
    run_bot()
