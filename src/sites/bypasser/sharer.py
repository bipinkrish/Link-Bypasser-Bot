"""
Sharer bypasser
"""

import re
import cloudscraper
from lxml import etree

# Site configuration
SITE_NAME = "Sharer"
URL_PATTERNS = [
    r'sharer\.pw/',
    r'sharer\.run/',
    r'sharer\.link/'
]

def parse_info_sharer(res):
    """
    Parse information from sharer page
    """
    info_parsed = {}
    title = re.findall('<h1 class="text-xl">(.*?)</h1>', res.text)
    info_parsed['title'] = title[0] if title else None
    return info_parsed

def sharer_bypass(url, Laravel_Session=None, XSRF_TOKEN=None):
    """
    Bypass Sharer short links
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        
        # Use provided credentials or empty fallback
        if Laravel_Session and XSRF_TOKEN:
            client.cookies.update(
                {"XSRF-TOKEN": XSRF_TOKEN, "laravel_session": Laravel_Session}
            )
            
        res = client.get(url)
        
        # Extract token
        token_matches = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)
        if not token_matches:
            return "Error: Could not find authentication token"
            
        token = token_matches[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
        
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
        }
        
        data = {"_token": token}
        
        # Try without login first
        data["nl"] = 1
        
        try:
            res = client.post(url + "/dl", headers=headers, data=data).json()
        except:
            return "Error: Failed to get download link from Sharer"
            
        if "url" in res and res["url"]:
            return res["url"]
            
        # If direct button exists and no login method worked
        if len(ddl_btn):
            return "Error: Sharer requires login credentials"
            
        return "Error: Could not bypass Sharer link"

    except Exception as e:
        return f"Error bypassing Sharer: {str(e)}"

# Common export function name  
process_url = sharer_bypass
