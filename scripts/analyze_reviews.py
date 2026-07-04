import pandas as pd

# Load the downloaded reviews
df = pd.read_csv("data/spotify_reviews.csv")

# Number of reviews to send to ChatGPT at one time
BATCH_SIZE = 100

print(f"Total Reviews: {len(df)}")

# Split reviews into batches
for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i:i+BATCH_SIZE]

    filename = f"output/reviews_batch_{i//BATCH_SIZE + 1}.csv"

    batch.to_csv(filename, index=False)

    print(f"Created {filename}")

print("\nAll review batches created successfully!")