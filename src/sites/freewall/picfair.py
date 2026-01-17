"""Picfair image downloader module"""

from core.utils import downloaderla, decrypt

SITE_NAME = "Picfair"
URL_PATTERNS = [r"picfair\.com"]

def process_url(url: str) -> str:
    """Download watermark-free images from Picfair
    
    Args:
        url: Picfair image URL
        
    Returns:
        Direct download link or error message
    """
    try:
        res = downloaderla(url, "https://downloader.la/picf.php")
        return decrypt(res, "?newURL=")
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
