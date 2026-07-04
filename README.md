# 🎵 Spotify Review Discovery Engine

## Overview

Spotify Review Discovery Engine is a review analytics project that collects user reviews from multiple sources and classifies them into meaningful categories using AI. The enriched dataset helps identify customer sentiment, music discovery challenges, user goals, and user segments, making it suitable for dashboards and product insights.

---

## Features

- Download Spotify reviews
- Download Reddit reviews
- Download App Store reviews (optional)
- AI-powered review classification
- Dashboard-ready CSV generation
- Product insight documentation

---

## Tech Stack

- Python 3.x
- Pandas
- OpenAI API
- Reddit API (PRAW)
- Google Play Scraper

---

## Project Structure

```
Spotify-Review-Discovery-Engine/
│
├── data/                  # Raw review datasets
├── docs/                  # Project documentation
├── output/                # Generated analysis and dashboard files
├── prompts/               # AI prompts
├── scripts/               # Python scripts
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

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Download Spotify Reviews

```bash
python scripts/download_reviews.py
```

### Download Reddit Reviews

```bash
python scripts/download_reddit.py
```

### Download App Store Reviews (Optional)

```bash
python scripts/download_appstore.py
```

### Analyze Reviews

```bash
python scripts/analyze_reviews.py
```

---

## Output

The generated files are available in the `output/` directory.

- analyzed_reviews.csv
- dashboard_data.csv
- reviews_batch_1.csv
- reviews_batch_2.csv

Each analyzed review contains:

- Review
- Rating
- Sentiment
- Problem Category
- Discovery Issue
- User Goal
- User Segment

---

## Documentation

Project documentation is available in the `docs/` folder.

- AI Workflow
- Architecture
- Dashboard Plan
- Feature PRD
- Findings
- Metrics
- Product Strategy
- User Journey
- User Personas
- Final Report

---

## Future Improvements

- Interactive Streamlit dashboard
- Real-time review ingestion
- Multi-language sentiment analysis
- Advanced topic modeling
- Recommendation quality metrics

---

## Author

**Vikas Sehrawat**