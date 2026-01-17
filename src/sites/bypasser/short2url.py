"""
Short2url bypasser
"""

import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Short2url"
URL_PATTERNS = [
    r'short2url\.in/',
    r'short2url\.com/'
]

def short2url_bypass(url):
    """
    Bypass Short2url short links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        DOMAIN = "https://techyuth.xyz/blog"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://blog.coin2pay.xyz/"
        h = {"referer": ref}
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(10)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return "Something went wrong with Short2url bypass"

    except Exception as e:
        return f"Error bypassing Short2url: {str(e)}"

# Common export function name
process_url = short2url_bypass
