"""
Gyanilinks bypasser
"""

import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "Gyanilinks"
URL_PATTERNS = [
    r'gyanilinks\.com/',
    r'go\.hipsonyc\.com/',
    r'gtlinks\.me/'
]

def gyanilinks_bypass(url):
    """
    Bypass Gyanilinks short links
    """
    try:
        DOMAIN = "https://go.hipsonyc.com/"
        client = cloudscraper.create_scraper(allow_brotli=False)
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        resp = client.get(final_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        try:
            inputs = soup.find(id="go-link").find_all(name="input")
        except:
            return "Incorrect Gyanilinks URL"
            
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(5)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return "Something went wrong with Gyanilinks bypass"

    except Exception as e:
        return f"Error bypassing Gyanilinks: {str(e)}"

# Common export function name
process_url = gyanilinks_bypass
