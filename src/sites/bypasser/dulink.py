"""Dulink URL bypasser module"""

try:
    import cloudscraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    BeautifulSoup = None

SITE_NAME = "Dulink"
URL_PATTERNS = [r"du-link\."]

def process_url(url: str) -> str:
    """Bypass Dulink shortened URLs
    
    Args:
        url: Dulink shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        DOMAIN = "https://du-link.in"
        url = url[:-1] if url[-1] == "/" else url
        ref = "https://profitshort.com/"
        h = {"referer": ref}
        
        resp = client.get(url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        
        h = {"x-requested-with": "XMLHttpRequest"}
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        return r.json()["url"]
    except Exception:
        return "Something went wrong :("
