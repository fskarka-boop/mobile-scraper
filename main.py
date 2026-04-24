import os
import json
import requests
from bs4 import BeautifulSoup

CHAT_ID = 1076519369
TOKEN = os.getenv("TELEGRAM_TOKEN")

URL = "https://suchen.mobile.de/fahrzeuge/search.html?vc=Car&seller=RSAUTOMOBILEGMBHHIRSCHAU&sort=NEW_FIRST"

SEEN_FILE = "seen.json"


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)


def check_new_listings():
   
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.select("a.result-item")

    seen = load_seen()
    new_seen = set(seen)

    for item in listings:
        href = item.get("href")
        if not href:
            continue

        link = "https://suchen.mobile.de" + href
        title = item.get("title", "Nový inzerát")
        ad_id = link.split("id=")[-1]

        if ad_id not in seen:
            send_message(f"🆕 Nový inzerát:\n{title}\n{link}")
            new_seen.add(ad_id)

    save_seen(new_seen)


if __name__ == "__main__":
    check_new_listings()
