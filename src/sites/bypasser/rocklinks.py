"""
RockLinks bypasser
"""

import requests
import time
import cloudscraper
from bs4 import BeautifulSoup

# Site configuration
SITE_NAME = "RockLinks"
URL_PATTERNS = [
    r'rocklinks\.net/',
    r'link\.urlwash\.org/'
]

def rocklinks_bypass(url):
    """
    Bypass RockLinks URLs
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        
        if "rocklinks.net" in url:
            DOMAIN = "https://blog.rocklinks.net"
        else:
            DOMAIN = "https://link.urlwash.org"

        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        
        if "rocklinks.net" in url:
            final_url = f"{DOMAIN}/{code}?quelle="
        else:
            final_url = f"{DOMAIN}/{code}"

        resp = client.get(final_url)
        soup = BeautifulSoup(resp.content, "html.parser")

        try:
            inputs = soup.find(id="go-link").find_all(name="input")
        except:
            return f"Could not find form in RockLinks page: {url}"

        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}

        time.sleep(10)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        try:
            return r.json()["url"]
        except:
            return f"Could not extract RockLinks URL: {url}"
            
    except Exception as e:
        return f"Error bypassing RockLinks: {str(e)}"

# Common export function name
process_url = rocklinks_bypass
