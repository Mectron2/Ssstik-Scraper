# Ssstik-Scraper
Ported from: https://github.com/TobyG74/tiktok-api-dl This repository contains a Python script designed to scrape video and photo content from TikTok using the SSSTik.io service. By providing a TikTok URL, the script retrieves detailed information about the media, including author details, statistics, and direct links to images or videos

Features
TikTok URL Validation: Ensures the provided URL is in the correct format for TikTok videos or photos.
Content Retrieval: Fetches and parses HTML content from SSSTik.io to extract media details.
Author Information: Extracts and includes author details such as avatar and nickname.
Media Statistics: Provides counts for likes, comments, and shares.
Media Type Detection: Differentiates between photo and video content, providing appropriate direct links.
Error Handling: Robust error handling for invalid URLs and network issues.

Usage

Clone the repository:
git clone https://github.com/yourusername/ssstik-scraper.git
cd ssstik-scraper

Install dependencies:
pip install requests beautifulsoup4
Run the script:

from scraper import scraper
url = "your_tiktok_url_here"
result = scraper(url)
print(result)
