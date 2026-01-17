"""
Alamy stock photo bypasser
"""

import requests
import base64

# Site configuration
SITE_NAME = "Alamy"
URL_PATTERNS = [
    r'alamy\.com/'
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
    Use downloader.la service
    """
    try:
        params = {
            "url": url,
        }
        return requests.get(site, params=params).json()
    except:
        return {"success": False}

def alamy_bypass(url):
    """
    Bypass Alamy watermarks
    """
    try:
        res = downloaderla(url, "https://new.downloader.la/alamy.php")
        result = decrypt(res, "#")
        
        if result:
            return result
        else:
            return "Error: Could not bypass Alamy watermark"

    except Exception as e:
        return f"Error bypassing Alamy: {str(e)}"

# Common export function name
process_url = alamy_bypass
