"""HXFile direct link generator module"""

from urllib.parse import urlparse
from requests import session

try:
    from bs4 import BeautifulSoup
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    BeautifulSoup = None

SITE_NAME = "HXFile"
URL_PATTERNS = [r"hxfile\."]

def process_url(url: str) -> str:
    """Generate direct download link for HXFile URLs
    
    Args:
        url: HXFile URL
        
    Returns:
        Direct download link or error message
    """
    if not DEPENDENCIES_AVAILABLE:
        return "ERROR: Required dependencies (beautifulsoup4) not available"
    
    sess = session()
    
    try:
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
        }

        # Extract file ID from URL path
        file_id = urlparse(url).path.strip("/")
        
        data = {
            "op": "download2",
            "id": file_id,
            "rand": "",
            "referer": "",
            "method_free": "",
            "method_premium": "",
        }

        response = sess.post(url, headers=headers, data=data)
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to find download button
        if btn := soup.find(class_="btn btn-dow"):
            return btn["href"]
        if unique := soup.find(id="uniqueExpirylink"):
            return unique["href"]
            
        return "ERROR: Download link not found"

    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
