"""HTSMovies URL bypasser module"""

import time

try:
    import cloudscraper
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    cloudscraper = None
    BeautifulSoup = None

SITE_NAME = "HTSMovies"
URL_PATTERNS = [r"htpmovies\.", r"htsmovies\."]

def process_url(link: str) -> str:
    """Bypass HTSMovies shortened URLs
    
    Args:
        link: HTSMovies shortened URL
        
    Returns:
        Original URL or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, beautifulsoup4) not available"
    
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        r = client.get(link, allow_redirects=True).text
        j = r.split('("')[-1]
        url = j.split('")')[0]
        param = url.split("/")[-1]
        
        DOMAIN = "https://go.theforyou.in"
        final_url = f"{DOMAIN}/{param}"
        resp = client.get(final_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        try:
            inputs = soup.find(id="go-link").find_all(name="input")
        except Exception:
            return "Incorrect Link"
            
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        time.sleep(10)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        
        return r.json()["url"]
    except Exception:
        return "Something went Wrong !!"
