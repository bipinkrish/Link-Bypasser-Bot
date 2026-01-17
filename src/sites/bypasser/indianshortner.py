"""IndianShortner URL bypasser module"""

import time

try:
    import cloudscraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    BeautifulSoup = None

SITE_NAME = "IndianShortner"
URL_PATTERNS = [r"indianshortner\."]

def process_url(url: str) -> str:
    """Bypass IndianShortner shortened URLs
    
    Args:
        url: IndianShortner shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        DOMAIN = "https://indianshortner.com/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://moddingzone.in/"
        h = {"referer": ref}
        
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(5)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        return r.json()["url"]
    except Exception:
        return "Something went wrong :("
