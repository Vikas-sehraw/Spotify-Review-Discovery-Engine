import os
import json
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# ==========================
# Load Gemini API Key
# ==========================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# ==========================
# Input & Output Files
# ==========================

INPUT_FILE = "data/spotify_reviews.csv"
OUTPUT_FILE = "outputs/analyzed_reviews.csv"

os.makedirs("outputs", exist_ok=True)

# ==========================
# Load Reviews
# ==========================

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df)} reviews")

# ==========================
# AI Review Analyzer
# ==========================

def analyze_review(review):

    prompt = f"""
You are an expert Product Manager analyzing Spotify user feedback.

Analyze the review and return ONLY valid JSON.

{{
  "sentiment":"",
  "problem_category":"",
  "discovery_issue":"",
  "user_goal":"",
  "user_segment":"",
  "feature_request":"",
  "unmet_need":""
}}

Definitions:

sentiment:
Positive / Neutral / Negative

problem_category:
Examples:
Recommendations
Ads
Premium
Podcasts
Downloads
Search
Playback
UI
Performance
Pricing
Library
Other

discovery_issue:
Explain why discovering music is difficult.

user_goal:
What is the user trying to achieve?

user_segment:
Examples:
Free User
Premium User
Heavy Listener
Casual Listener
Podcast Listener
Music Explorer
Student
Unknown

feature_request:
Requested feature, if any.

unmet_need:
Underlying need that Spotify isn't fulfilling.

Review:
\"\"\"{review}\"\"\"

Return JSON only.
"""

    for attempt in range(3):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(text)

        except Exception as e:

            print(f"Retry {attempt+1}/3")

            if attempt == 2:

                print(e)

                return {
                    "sentiment": "",
                    "problem_category": "",
                    "discovery_issue": "",
                    "user_goal": "",
                    "user_segment": "",
                    "feature_request": "",
                    "unmet_need": ""
                }

            time.sleep(3)

# ==========================
# Process Reviews
# ==========================

results = []

for index, row in df.iterrows():

    print(f"[{index+1}/{len(df)}] Processing...")

    review = str(row["Review"])

    analysis = analyze_review(review)

    results.append({
        **row.to_dict(),
        **analysis
    })

    # Save every 10 reviews
    if (index + 1) % 10 == 0:

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(f"Saved progress ({index+1} reviews)")

    # Small delay to avoid hitting rate limits
    time.sleep(1)

# ==========================
# Save Final Output
# ==========================

output = pd.DataFrame(results)

output.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n====================================")
print("Analysis Complete!")
print(f"Total Reviews: {len(output)}")
print(f"Saved to: {OUTPUT_FILE}")
print("====================================")