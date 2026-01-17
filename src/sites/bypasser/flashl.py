"""
Flashlink bypasser
"""

import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Flashlink"
URL_PATTERNS = [
    r'files\.earnash\.com/',
    r'flash1\.cordtpoint\.co\.in/'
]

def flashl_bypass(url):
    """
    Bypass Flashlink short links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        DOMAIN = "https://files.earnash.com/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://flash1.cordtpoint.co.in"
        h = {"referer": ref}
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(15)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return "Something went wrong with Flashlink bypass"

    except Exception as e:
        return f"Error bypassing Flashlink: {str(e)}"

# Common export function name
process_url = flashl_bypass
