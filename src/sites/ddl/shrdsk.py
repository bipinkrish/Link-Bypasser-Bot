"""Shrdsk direct link generator module"""

try:
    from cloudscraper import create_scraper
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    create_scraper = None

SITE_NAME = "Shrdsk"
URL_PATTERNS = [r"shrdsk\."]

def process_url(url: str) -> str:
    """Generate direct download link for Shrdsk URLs
    
    Args:
        url: Shrdsk URL
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper) not available"
    
    cget = create_scraper().request
    
    try:
        url = cget("GET", url).url
        res = cget(
            "GET",
            f'https://us-central1-affiliate2apk.cloudfunctions.net/get_data?shortid={url.split("/")[-1]}',
        )
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
        
    if res.status_code != 200:
        return f"ERROR: Status Code {res.status_code}"
        
    res = res.json()
    if "type" in res and res["type"].lower() == "upload" and "video_url" in res:
        return res["video_url"]
        
    return "ERROR: cannot find direct link"
