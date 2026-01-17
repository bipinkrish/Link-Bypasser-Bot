"""Linkbox direct link generator module"""

from urllib.parse import quote

try:
    from cloudscraper import create_scraper
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    create_scraper = None

SITE_NAME = "Linkbox"
URL_PATTERNS = [r"linkbox\."]

def process_url(url: str) -> str:
    """Generate direct download link for Linkbox URLs
    
    Args:
        url: Linkbox URL
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper) not available"
    
    cget = create_scraper().request
    
    try:
        url = cget("GET", url).url
        res = cget(
            "GET", f'https://www.linkbox.to/api/file/detail?itemId={url.split("/")[-1]}'
        ).json()
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
        
    if "data" not in res:
        return "ERROR: Data not found!!"
        
    data = res["data"]
    if not data:
        return "ERROR: Data is None!!"
        
    if "itemInfo" not in data:
        return "ERROR: itemInfo not found!!"
        
    itemInfo = data["itemInfo"]
    if "url" not in itemInfo:
        return "ERROR: url not found in itemInfo!!"
        
    if "name" not in itemInfo:
        return "ERROR: Name not found in itemInfo!!"
        
    name = quote(itemInfo["name"])
    raw = itemInfo["url"].split("/", 3)[-1]
    
    return f"https://wdl.nuplink.net/{raw}&filename={name}"
