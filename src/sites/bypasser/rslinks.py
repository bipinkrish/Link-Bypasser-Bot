"""RSLinks URL bypasser module"""

import requests

SITE_NAME = "RSLinks"
URL_PATTERNS = [r"rslinks\."]

def process_url(url: str) -> str:
    """Bypass RSLinks shortened URLs
    
    Args:
        url: RSLinks shortened URL
        
    Returns:
        Original URL or error message
    """
    try:
        client = requests.session()
        download = requests.get(url, stream=True, allow_redirects=False)
        v = download.headers["location"]
        code = v.split("ms9")[-1]
        final = f"http://techyproio.blogspot.com/p/short.html?{code}=="
        return final
    except Exception:
        return "Something went wrong :("
