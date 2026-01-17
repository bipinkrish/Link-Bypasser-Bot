"""AKMFiles direct link generator module"""

try:
    from cloudscraper import create_scraper
    from lxml import etree
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    create_scraper = None
    etree = None

SITE_NAME = "AKMFiles"
URL_PATTERNS = [r"akmfiles\."]

def process_url(url: str) -> str:
    """Generate direct download link for AKMFiles URLs
    
    Args:
        url: AKMFiles URL
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (cloudscraper, lxml) not available"
    
    cget = create_scraper().request
    
    try:
        url = cget("GET", url).url
        json_data = {"op": "download2", "id": url.split("/")[-1]}
        res = cget("POST", url, data=json_data)
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
        
    html_tree = etree.HTML(res.content)
    direct_link = html_tree.xpath("//a[contains(@class,'btn btn-dow')]/@href")
    
    if direct_link:
        return direct_link[0]
    else:
        return "ERROR: Direct link not found"
