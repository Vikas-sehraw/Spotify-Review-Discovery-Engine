# AI Review Discovery Engine Workflow

## Objective

Analyze user feedback from multiple platforms and convert unstructured reviews into structured product insights.

---

## Input Sources

- Google Play Reviews
- Apple App Store Reviews
- Reddit Discussions
- Spotify Community
- Social Media

---

## AI Processing Pipeline

### Step 1: Data Collection

Collect reviews from all available sources.

Output:

combined_reviews.csv

---

### Step 2: Prompt Engineering

Each review is sent to an LLM with a structured prompt.

The model extracts:

- Sentiment
- Problem Category
- User Goal
- Root Cause
- Discovery Issue
- User Segment
- Severity
- Suggested Improvement

---

### Step 3: Structured Dataset

The AI converts free-text reviews into structured records.

Output:

analyzed_reviews.csv

---

### Step 4: Analytics

The structured dataset is analyzed to identify:

- recurring issues
- user behavior
- unmet needs
- feature opportunities

---

### Step 5: Product Decision

Insights are converted into product recommendations for Spotify's Growth Team.