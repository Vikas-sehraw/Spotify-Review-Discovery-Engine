# 🎵 Spotify AI Review Discovery Engine

## Overview

Spotify AI Review Discovery Engine is an AI-powered review analytics system that collects user feedback from multiple platforms and automatically transforms unstructured reviews into structured product insights using Google's Gemini AI.

The system analyzes reviews from Google Play, Reddit, and the App Store to identify customer sentiment, music discovery challenges, recommendation frustrations, user goals, listening behaviors, feature requests, user segments, and unmet needs. The enriched dataset can be used for dashboards, product research, and product management decision-making.

---

## Features

- Collect Spotify reviews from Google Play
- Collect Reddit discussions
- Collect App Store reviews (optional)
- Merge reviews into a unified dataset
- AI-powered review analysis using Gemini 2.5 Flash
- Automatic sentiment classification
- Identify music discovery challenges
- Detect recommendation frustrations
- Extract user goals and listening behaviors
- Classify user segments
- Identify feature requests
- Discover unmet user needs
- Generate dashboard-ready CSV files

---

## AI Review Discovery Pipeline

```
Google Play Reviews
          │
Reddit Discussions
          │
App Store Reviews
          │
          ▼
Combined Review Dataset
          ▼
Gemini AI Review Analyzer
          ▼
Structured Product Insights
          ▼
Dashboard-ready CSV
```

---

## Product Questions Answered

The AI-powered review discovery engine helps answer:

- Why do users struggle to discover new music?
- What are the most common frustrations with recommendations?
- What listening behaviors are users trying to achieve?
- What causes users to repeatedly listen to the same content?
- Which user segments experience different discovery challenges?
- What unmet needs consistently emerge across reviews?
- Which product improvements are requested most frequently?

---

## Tech Stack

- Python 3.x
- Pandas
- Google Gemini 2.5 Flash API
- Python Dotenv
- Google Play Scraper
- Reddit API (PRAW)
- App Store Scraper

---

## Project Structure

```
Spotify-Review-Discovery-Engine/
│
├── data/                      # Raw and merged review datasets
├── docs/                      # Project documentation
├── outputs/                   # AI-generated analysis
├── prompts/                   # AI prompts
├── scripts/
│   ├── download_reviews.py
│   ├── download_reddit.py
│   ├── download_appstore.py
│   ├── merge_reviews.py
│   └── analyze_reviews.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Vikas-sehraw/Spotify-Review-Discovery-Engine.git
cd Spotify-Review-Discovery-Engine
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Running the Project

### Download Google Play Reviews

```bash
python scripts/download_reviews.py
```

### Download Reddit Discussions

```bash
python scripts/download_reddit.py
```

### Download App Store Reviews (Optional)

```bash
python scripts/download_appstore.py
```

### Merge Review Sources

```bash
python scripts/merge_reviews.py
```

### Analyze Reviews Using Gemini AI

```bash
python scripts/analyze_reviews.py
```

---

## AI Output

The AI automatically enriches every review with structured product insights.

Each analyzed review contains:

| Field | Description |
|--------|-------------|
| Review | Original review text |
| Rating | User rating |
| Sentiment | Positive, Neutral or Negative |
| Problem Category | Primary issue category |
| Discovery Issue | Music discovery challenge |
| User Goal | User's intended outcome |
| User Segment | Listener type |
| Feature Request | Requested improvement |
| Unmet Need | Underlying customer need |

---

## Output Files

Generated files are available in the `outputs/` directory.

- analyzed_reviews.csv
- dashboard_data.csv
- combined_reviews.csv

These files can be directly used for:

- Product dashboards
- User research
- Product requirement documents
- Feature prioritization
- Customer insight reports

---

## Documentation

The `docs/` folder contains:

- AI Workflow
- System Architecture
- Dashboard Plan
- Product Requirements Document (PRD)
- Product Findings
- Product Metrics
- Product Strategy
- User Journey
- User Personas
- Final Report

---

## Future Improvements

- Interactive Streamlit dashboard
- Real-time review ingestion
- Support for additional social media platforms
- Multi-language review analysis
- Topic clustering and trend detection
- Recommendation quality metrics
- Automated insight summarization

---

## Author

**Vikas Sehrawat**