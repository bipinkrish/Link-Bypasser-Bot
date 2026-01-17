"""Adrinolinks URL bypasser module"""

import time

try:
    import cloudscraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    BeautifulSoup = None

SITE_NAME = "Adrinolinks"
URL_PATTERNS = [r"adrinolinks\."]

def process_url(url: str) -> str:
    """Bypass Adrinolinks shortened URLs
    
    Args:
        url: Adrinolinks shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    try:
        # Normalize URL format
        if "https://adrinolinks.in/" not in url:
            url = "https://adrinolinks.in/" + url.split("/")[-1]
            
        client = cloudscraper.create_scraper(allow_brotli=False)
        DOMAIN = "https://adrinolinks.in"
        ref = "https://wikitraveltips.com/"
        h = {"referer": ref}
        
        resp = client.get(url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(8)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        return r.json()["url"]
    except Exception:
        return "Something went wrong :("
