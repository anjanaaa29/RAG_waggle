import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://support.mywaggle.com"
OUTPUT_FILE = "data/faqs.txt"

# List of FAQ pages to scrape
FAQ_PAGES = [
    "/",
    "/waggle-faq",
    "/wagglecam-faq",
    "/waggle-wifi-camera-faq",
    "/smart-sensor-faq",
    "/smart-feeder-faq"
]

def scrape_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def main():
    os.makedirs("data", exist_ok=True)

    all_text = []

    for page in FAQ_PAGES:
        full_url = BASE_URL + page
        print(f"Scraping: {full_url}")

        try:
            page_text = scrape_page(full_url)
            all_text.append(f"\n--- SOURCE: {full_url} ---\n")
            all_text.append(page_text)
        except Exception as e:
            print(f"Failed to scrape {full_url}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))

    print(f"\nSaved FAQ text to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

