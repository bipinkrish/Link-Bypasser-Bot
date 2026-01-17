"""
Getty Images bypasser
"""

import requests
import base64

# Site configuration
SITE_NAME = "Getty Images"
URL_PATTERNS = [
    r'gettyimages\.',
    r'istockphoto\.com/'
]

def decrypt(res, key):
    """
    Decrypt response from downloader service
    """
    if res.get("success"):
        return base64.b64decode(res["result"].split(key)[-1]).decode("utf-8")
    return None

def downloaderla(url, site):
    """
    Use downloader service
    """
    try:
        params = {
            "url": url,
        }
        return requests.get(site, params=params).json()
    except:
        return {"success": False}

def getty_bypass(url):
    """
    Bypass Getty Images watermarks
    """
    try:
        res = downloaderla(url, "https://getpaidstock.com/api.php")
        result = decrypt(res, "#")
        
        if result:
            return result
        else:
            return "Error: Could not bypass Getty Images watermark"

    except Exception as e:
        return f"Error bypassing Getty Images: {str(e)}"

# Common export function name
process_url = getty_bypass
