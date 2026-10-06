from datetime import datetime, timezone
from typing import Iterator, Dict, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import BaseScraper

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL


class BooksScraper(BaseScraper):
    """Scrapes all available pages from Books to Scrape."""

    def scrape(self) -> Iterator[Dict[str, Any]]:
        url = START_URL
        page_number = 0

        while url:
            page_number += 1
            html = self.fetch(url)
            soup = BeautifulSoup(html, "html.parser")

            for card in soup.select("article.product_pod"):
                title_el = card.select_one("h3 a")
                price_el = card.select_one(".price_color")
                availability_el = card.select_one(".availability")
                rating_el = card.select_one("p.star-rating")
                category_el = card.select_one("p.instock")  # source-specific fallback

                if not title_el:
                    continue

                rating = None
                if rating_el:
                    classes = rating_el.get("class", [])
                    rating_names = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                    for name, value in rating_names.items():
                        if name in classes:
                            rating = value
                            break

                availability = availability_el.get_text(" ", strip=True) if availability_el else None
                price = price_el.get_text(" ", strip=True) if price_el else None

                detail_url = (
                    urljoin(url, title_el.get("href"))
                    if title_el.get("href")
                    else None
                )

                yield {
                    "source": "Books to Scrape",
                    "source_url": detail_url or url,
                    "name_or_title": title_el.get("title") or title_el.get_text(" ", strip=True),
                    "category": None,
                    "price": price,
                    "rating": rating,
                    "author": None,
                    "tags": None,
                    "description": availability,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "_page": page_number,
                }

            next_link = soup.select_one("li.next a")
            url = urljoin(url, next_link.get("href")) if next_link and next_link.get("href") else None
