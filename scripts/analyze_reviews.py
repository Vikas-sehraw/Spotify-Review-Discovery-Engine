import os
import re
import json
import time
import random
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# ============================================================
# CONFIGURATION
# ============================================================

BATCH_SIZE = 1
MAX_RETRIES = 3
SAVE_AFTER_BATCH = True
DELAY_BETWEEN_BATCHES = 4

INPUT_FILE = "data/combined_reviews.csv"
OUTPUT_FILE = "output/analyzed_reviews.csv"

os.makedirs("output", exist_ok=True)

# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# FIXED ENUMS
# ============================================================

SENTIMENTS = [
    "Positive",
    "Neutral",
    "Negative"
]

PROBLEM_CATEGORIES = [
    "Recommendations",
    "Discovery",
    "Playback",
    "Search",
    "Library",
    "Ads",
    "Premium",
    "Pricing",
    "Downloads",
    "Podcasts",
    "Performance",
    "UI",
    "Other"
]

DISCOVERY_ISSUES = [
    "Recommendation Fatigue",
    "Poor Personalization",
    "Limited Genre Diversity",
    "Hard to Discover New Artists",
    "External Discovery",
    "No Discovery Issue"
]

USER_GOALS = [
    "Discover New Music",
    "Workout",
    "Relaxation",
    "Study",
    "Commute",
    "Focus",
    "Sleep",
    "Podcast Listening",
    "Create Playlist",
    "General Listening"
]

USER_SEGMENTS = [
    "Free User",
    "Premium User",
    "Heavy Listener",
    "Casual Listener",
    "Music Explorer",
    "Student",
    "Podcast Listener",
    "Unknown"
]

# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(INPUT_FILE)

reviews_df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("Spotify Review Discovery Engine")
print("=" * 60)
print(f"Loaded {len(reviews_df)} reviews")

# ============================================================
# RESUME SUPPORT
# ============================================================

processed_reviews = []

processed_ids = set()

if os.path.exists(OUTPUT_FILE):

    existing = pd.read_csv(OUTPUT_FILE)

    processed_reviews = existing.to_dict("records")

    if "Review" in existing.columns:
        processed_ids = set(existing["Review"].astype(str))

    print(f"Resuming from {len(processed_reviews)} completed reviews")

else:

    print("Starting fresh analysis")

print("=" * 60)
# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text: str):

    if not text:
        return None

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        pass

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None


# ============================================================
# DEFAULT RESULT
# ============================================================

def default_result():

    return {
        "sentiment": "Unknown",
        "problem_category": "Other",
        "discovery_issue": "No Discovery Issue",
        "user_goal": "General Listening",
        "user_segment": "Unknown",
        "feature_request": "",
        "unmet_need": ""
    }


# ============================================================
# BUILD PROMPT
# ============================================================

def build_prompt(batch_reviews):

    review_text = ""

    for i, review in enumerate(batch_reviews):

        review_text += f"""
Review {i+1}
{review}

"""

    prompt = f"""
You are a Senior Product Manager at Spotify.

Every review below is a real Spotify user review collected from the Play Store, App Store, Reddit or Spotify Community.

Analyze each review independently from a Product Management perspective.

Use ONLY the allowed values listed below.

If there is no feature request, return an empty string.

If there is no discovery issue, return "No Discovery Issue".

Return ONLY valid JSON.

Do not use markdown.

Do not explain anything.

Return exactly ONE JSON object.

Each object MUST contain EXACTLY these keys.

{{
"sentiment":"",
"problem_category":"",
"discovery_issue":"",
"user_goal":"",
"user_segment":"",
"feature_request":"",
"unmet_need":""
}}

Allowed Sentiment:

{", ".join(SENTIMENTS)}

Allowed Problem Categories:

{", ".join(PROBLEM_CATEGORIES)}

Allowed Discovery Issues:

{", ".join(DISCOVERY_ISSUES)}

Allowed User Goals:

{", ".join(USER_GOALS)}

Allowed User Segments:

{", ".join(USER_SEGMENTS)}

Feature Request:
Short phrase only.

Unmet Need:
One short sentence.

Reviews:

{review_text}

Return ONLY JSON.

Do NOT explain anything.

Do NOT use markdown.
"""

    return prompt


# ============================================================
# GEMINI BATCH ANALYSIS
# ============================================================

def analyze_batch(batch_reviews):

    prompt = build_prompt(batch_reviews)

    for attempt in range(MAX_RETRIES):

        try:

            print("Sending request to Gemini...")

            response = model.generate_content(
                prompt,
                request_options={"timeout": 30}
            )

            print("Response received.")

            parsed = extract_json(response.text)

            if parsed is None:
                raise Exception("Could not parse Gemini JSON.")

           

            if isinstance(parsed, dict):
                return [parsed]

            if isinstance(parsed, list):
                return parsed[:1]

            raise Exception("Gemini returned invalid JSON.")
        except Exception as e:

            print(
                f"Retry {attempt + 1}/{MAX_RETRIES} "
                f"failed: {str(e)}"
            )

            if attempt < MAX_RETRIES - 1:

                wait = 35

                print("\n===================================")
                print("⚠️ Gemini API Rate Limit Reached")
                print(f"Retrying in {wait} seconds...")
                print("===================================\n")

                time.sleep(wait)

            else:

                print("\n===================================")
                print("❌ Maximum retries reached")
                print("Using default values for this review.")
                print("===================================\n")

                return [default_result()]


# ============================================================
# VALIDATION
# ============================================================

def normalize(record):

    # -------------------------
    # Sentiment
    # -------------------------
    record["sentiment"] = str(
        record.get("sentiment", "")
    ).strip().title()

    if record["sentiment"] not in SENTIMENTS:
        record["sentiment"] = "Unknown"

    # -------------------------
    # Problem Category
    # -------------------------
    record["problem_category"] = str(
        record.get("problem_category", "")
    ).strip().title()

    if record["problem_category"] not in PROBLEM_CATEGORIES:
        record["problem_category"] = "Other"

    # -------------------------
    # Discovery Issue
    # -------------------------
    record["discovery_issue"] = str(
        record.get("discovery_issue", "")
    ).strip().title()

    valid_discovery = {
        d.title(): d for d in DISCOVERY_ISSUES
    }

    if record["discovery_issue"] in valid_discovery:
        record["discovery_issue"] = valid_discovery[
            record["discovery_issue"]
        ]
    else:
        record["discovery_issue"] = "No Discovery Issue"

    # -------------------------
    # User Goal
    # -------------------------
    record["user_goal"] = str(
        record.get("user_goal", "")
    ).strip().title()

    valid_goals = {
        g.title(): g for g in USER_GOALS
    }

    if record["user_goal"] in valid_goals:
        record["user_goal"] = valid_goals[
            record["user_goal"]
        ]
    else:
        record["user_goal"] = "General Listening"

    # -------------------------
    # User Segment
    # -------------------------
    record["user_segment"] = str(
        record.get("user_segment", "")
    ).strip().title()

    valid_segments = {
        s.title(): s for s in USER_SEGMENTS
    }

    if record["user_segment"] in valid_segments:
        record["user_segment"] = valid_segments[
            record["user_segment"]
        ]
    else:
        record["user_segment"] = "Unknown"

    # -------------------------
    # Feature Request
    # -------------------------
    record["feature_request"] = str(
        record.get("feature_request", "")
    ).strip()

    # -------------------------
    # Unmet Need
    # -------------------------
    record["unmet_need"] = str(
        record.get("unmet_need", "")
    ).strip()

    return record


# ============================================================
# REMOVE ALREADY PROCESSED REVIEWS
# ============================================================

pending_reviews = reviews_df[
    ~reviews_df["Review"].astype(str).isin(processed_ids)
].copy()

pending_reviews.reset_index(
    drop=True,
    inplace=True
)

print(
    f"Remaining reviews: {len(pending_reviews)}"
)

# ============================================================
# PROCESS IN BATCHES
# ============================================================

total = len(pending_reviews)

for start in range(0, total, BATCH_SIZE):

    end = min(start + BATCH_SIZE, total)

    batch_df = pending_reviews.iloc[start:end]

    batch_reviews = (
        batch_df["Review"]
        .fillna("")
        .astype(str)
        .tolist()
    )

    print(
        f"\nProcessing "
        f"{start + 1}-{end} of {total}"
    )

    analysis = analyze_batch(batch_reviews)

    for (_, row), result in zip(
        batch_df.iterrows(),
        analysis
    ):

        result = normalize(result)

        processed_reviews.append({

            **row.to_dict(),

            **result

        })
    # ========================================================
    # SAVE AFTER EVERY BATCH
    # ========================================================

    if SAVE_AFTER_BATCH:

        output_df = pd.DataFrame(processed_reviews)

        output_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(
            f"Saved {len(output_df)} reviews"
        )

    time.sleep(DELAY_BETWEEN_BATCHES)

# ============================================================
# FINAL SAVE
# ============================================================

output_df = pd.DataFrame(processed_reviews)

output_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("AI REVIEW ANALYSIS COMPLETED")
print("=" * 70)

print(f"Total Reviews Processed : {len(output_df)}")

# ============================================================
# PRINT DISTRIBUTIONS
# ============================================================

summary_columns = [
    "sentiment",
    "problem_category",
    "discovery_issue",
    "user_goal",
    "user_segment"
]

for column in summary_columns:

    print("\n")
    print("=" * 70)
    print(column.upper())
    print("=" * 70)

    counts = (
        output_df[column]
        .fillna("Unknown")
        .value_counts()
    )

    print(counts)

# ============================================================
# EXPORT DASHBOARD SUMMARY
# ============================================================

dashboard_rows = []

for column in summary_columns:

    counts = (
        output_df[column]
        .fillna("Unknown")
        .value_counts()
    )

    total = counts.sum()

    for label, value in counts.items():

        dashboard_rows.append({

            "Category": column,

            "Label": label,

            "Count": int(value),

            "Percentage": round(
                (value / total) * 100,
                2
            )

        })

dashboard_df = pd.DataFrame(dashboard_rows)

dashboard_file = "output/dashboard_summary.csv"

dashboard_df.to_csv(
    dashboard_file,
    index=False
)

print("\n")
print("=" * 70)
print("FILES GENERATED")
print("=" * 70)
print(f"✔ Review Analysis : {OUTPUT_FILE}")
print(f"✔ Dashboard Data  : {dashboard_file}")
print("=" * 70)

print("\nTop Discovery Issues\n")

print(
    output_df["discovery_issue"]
    .value_counts()
    .head(10)
)

print("\nTop Problem Categories\n")

print(
    output_df["problem_category"]
    .value_counts()
    .head(10)
)

print("\nTop User Segments\n")

print(
    output_df["user_segment"]
    .value_counts()
    .head(10)
)

print("\nDone!")