"""MDisk Pro link bypasser module"""

import time

try:
    import cloudscraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    BeautifulSoup = None

SITE_NAME = "MDisk Pro"
URL_PATTERNS = [r"mdisk\.pro"]

def process_url(url: str) -> str:
    """Bypass MDisk Pro shortened URLs
    
    Args:
        url: MDisk Pro shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://mdisk.pro"
    ref = "https://m.meclipstudy.in/"
    h = {"referer": ref}
    
    try:
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
