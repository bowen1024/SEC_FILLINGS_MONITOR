import requests
import json
import logging

def fetch_filings(cik):
    padded_cik = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"

    headers = {
        "User-Agent": "abclimited (abclimited@gmail.com)",
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov"
    }

    try:
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        response.raise_for_status()
        # Parse JSON content
        data = response.json()
        return data.get('filings', {}).get('recent', {})

    except Exception as e:
        logging.error(f"SEC API error for CIK {cik}: {e}")
        return None