import asyncio
import random
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from src.db.manager import DBManager

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

class RentalScraper:
    def __init__(self, db: DBManager):
        self.db = db

    async def scrape_city(self, city_name: str):
        # Caching check: skip cities updated within the last 24 hours
        last_scraped = self.db.get_last_scraped_at(city_name)
        if last_scraped:
            # sqlite3 DATETIME is usually a string. Let's handle common formats.
            try:
                scraped_dt = datetime.fromisoformat(last_scraped) if isinstance(last_scraped, str) else datetime.now()
                if datetime.now() - scraped_dt < timedelta(hours=24):
                    print(f"Skipping {city_name}, already updated within 24h.")
                    return
            except ValueError:
                pass

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
            page = await context.new_page()
            
            # This is a generic search simulation for MVP
            # In real scenario, we would target specific portal selectors (e.g. Zonaprop, MercadoLibre)
            search_url = f"https://www.google.com/search?q=alquiler+departamento+{city_name}+argentina"
            await page.goto(search_url, timeout=30000)
            
            # Small delay to avoid bot detection
            await asyncio.sleep(random.uniform(2, 5))
            
            # Mock extracting data since portals have complex dynamic loads
            # In production, we'd use specific selectors for the targeted portal
            # For MVP, we simulate the finding of representative prices
            mock_prices = [random.uniform(200000, 450000), random.uniform(200000, 450000)]
            for price in mock_prices:
                self.db.save_rental(city_name, price, "ARS", "simulated_url")
                
            await browser.close()
 
    async def run(self, cities: list):
        for city in cities:
            print(f"Scrapeando {city}...")
            await self.scrape_city(city)
            await asyncio.sleep(random.uniform(1, 3))
