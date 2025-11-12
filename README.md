# Data Scraping from Reddit
## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`

## How to scrape
1. Fill in your API keys, keywords, and subreddits in `script.py`
2. Run `python script.py`
2. The data will be saved to `crawl_reddit.csv`
