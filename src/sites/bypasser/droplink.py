"""
Droplink bypasser
"""

import re
import time
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Site configuration
SITE_NAME = "Droplink"
URL_PATTERNS = [
    r'droplink\.co/',
    r'droplinks\.co/'
]

def droplink_bypass(url):
    """
    Bypass Droplink short links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        res = client.get(url, timeout=5)

        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
        h = {"referer": ref}
        res = client.get(url, headers=h)

        bs4 = BeautifulSoup(res.content, "html.parser")
        inputs = bs4.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
        }

        p = urlparse(url)
        final_url = f"{p.scheme}://{p.netloc}/links/go"
        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()

        if res["status"] == "success":
            return res["url"]
        return "Something went wrong with Droplink bypass"

    except Exception as e:
        return f"Error bypassing Droplink: {str(e)}"

# Common export function name
process_url = droplink_bypass
