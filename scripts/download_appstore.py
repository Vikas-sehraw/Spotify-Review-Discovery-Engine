from app_store_scraper import AppStore
import pandas as pd

print("Downloading App Store Reviews...")

app = AppStore(
    country="us",
    app_name="spotify-music-and-podcasts",
    app_id=324684580
)

app.review(how_many=200)

reviews = []

for review in app.reviews:

    reviews.append({
        "User": review["userName"],
        "Rating": review["rating"],
        "Review": review["review"],
        "Date": review["date"]
    })

df = pd.DataFrame(reviews)

df.to_csv("data/appstore_reviews.csv", index=False)

print(f"Downloaded {len(df)} App Store Reviews")