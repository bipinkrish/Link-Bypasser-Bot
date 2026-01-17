"""OneDrive direct link generator module"""

from urllib.parse import urlparse
from base64 import standard_b64encode

try:
    from cloudscraper import create_scraper
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    create_scraper = None

SITE_NAME = "OneDrive"
URL_PATTERNS = [r"1drv\.ms", r"onedrive\.live\.com"]

def process_url(link: str) -> str:
    """Generate direct download link for OneDrive URLs
    
    Based on https://github.com/UsergeTeam/Userge
    
    Args:
        link: OneDrive share URL
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper) not available"
    
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(
        standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8"
    )
    direct_link1 = (
        f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    )
    cget = create_scraper().request
    
    try:
        resp = cget("head", direct_link1)
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
        
    if resp.status_code != 302:
        return "ERROR: Unauthorized link, the link may be private"
        
    return resp.next.url
