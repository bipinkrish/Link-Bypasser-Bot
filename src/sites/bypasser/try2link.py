"""
Try2Link bypasser
"""

import requests
import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Try2Link"
URL_PATTERNS = [
    r'try2link\.com/',
    r'try2link\.net/'
]

def try2link_bypass(url):
    """
    Bypass Try2Link URLs
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)

        url = url[:-1] if url[-1] == "/" else url

        params = (("d", int(time.time()) + (60 * 4)),)
        r = client.get(url, params=params, headers={"Referer": "https://newforex.online/"})

        soup = BeautifulSoup(r.text, "html.parser")
        inputs = soup.find(id="go-link").find_all(name="input")
        data = {input.get("name"): input.get("value") for input in inputs}
        time.sleep(7)

        headers = {
            "Host": "try2link.com",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://try2link.com",
            "Referer": url,
        }

        bypassed_url = client.post(
            "https://try2link.com/links/go", headers=headers, data=data
        )
        return bypassed_url.json()["url"]
        
    except Exception as e:
        return f"Error bypassing Try2Link: {str(e)}"

# Common export function name
process_url = try2link_bypass
