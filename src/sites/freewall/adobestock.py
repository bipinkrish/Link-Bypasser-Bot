"""Adobe Stock image downloader module"""

from core.utils import downloaderla, decrypt

SITE_NAME = "Adobe Stock"
URL_PATTERNS = [r"stock\.adobe\.com"]

def process_url(url: str) -> str:
    """Download watermark-free images from Adobe Stock
    
    Args:
        url: Adobe Stock image URL
        
    Returns:
        Direct download link or error message
    """
    try:
        res = downloaderla(url, "https://new.downloader.la/adobe.php")
        return decrypt(res, "#")
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
