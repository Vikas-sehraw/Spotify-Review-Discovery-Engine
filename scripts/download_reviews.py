from google_play_scraper import reviews
import pandas as pd

print("Downloading Spotify reviews...")

result, continuation_token = reviews(
    "com.spotify.music",
    lang="en",
    country="us",
    count=500
)

data = []

for review in result:
    data.append({
        "User": review["userName"],
        "Rating": review["score"],
        "Review": review["content"],
        "Likes": review["thumbsUpCount"],
        "Date": review["at"]
    })

df = pd.DataFrame(data)

df.to_csv("data/spotify_reviews.csv", index=False)

print("Done!")
print(f"Downloaded {len(df)} reviews.")