#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Indi bypasser (Indian shortener)
Bypasses file.earnash.com links (indiurl)

Site: file.earnash.com (indiurl)
Method: Form submission with 10-second delay
"""

import time
try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False

# Site configuration
SITE_NAME = "indi"
URL_PATTERNS = [
    r'file\.earnash\.com',
    r'indiurl\.cordtpoint\.co\.in'
]

def process_url(url: str) -> str:
    """
    Bypass indi/indiurl URLs
    
    Args:
        url: file.earnash.com or indiurl URL
        
    Returns:
        Bypassed URL or error message
    """
    if not SCRAPER_AVAILABLE:
        return "ERROR: requests and bs4 modules not available"
    
    try:
        client = requests.session()
        DOMAIN = "https://file.earnash.com/"
        url = url[:-1] if url[-1] == "/" else url
        code = url.split("/")[-1]
        final_url = f"{DOMAIN}/{code}"
        ref = "https://indiurl.cordtpoint.co.in/"
        h = {"referer": ref}
        
        resp = client.get(final_url, headers=h)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {"x-requested-with": "XMLHttpRequest"}
        
        time.sleep(10)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
        try:
            return r.json()["url"]
        except:
            return "ERROR: Failed to extract URL from JSON response"
            
    except Exception as e:
        return f"ERROR: {e.__class__.__name__}"
