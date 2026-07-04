import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

search_terms = [
    "spotify recommendations",
    "spotify discover weekly",
    "spotify algorithm",
    "spotify new music"
]

posts = []

for term in search_terms:

    print(f"Searching: {term}")

    url = f"https://old.reddit.com/search/?q={term.replace(' ', '%20')}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch page")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("div", class_="search-result")

    for result in results:

        title = result.find("a", class_="search-title")

        if title:
            posts.append({
                "Source": "Reddit",
                "Keyword": term,
                "Title": title.text.strip(),
                "URL": title["href"]
            })

    time.sleep(2)

df = pd.DataFrame(posts)

df.to_csv("data/reddit_reviews.csv", index=False)

print(f"\nDownloaded {len(df)} Reddit posts")